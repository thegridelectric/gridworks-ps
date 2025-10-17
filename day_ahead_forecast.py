import csv
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Optional

import dotenv
import pendulum
import requests
from gwprice.asl.types import Price
from gwprice.config import Settings
from gwprice.models import HourlyPriceForecastSql
from gwprice.my_markets import MyMarkets
from gwprice.my_p_nodes import MyPNodes
from requests.auth import HTTPBasicAuth


def fetch_with_retry(
    url: str, auth: HTTPBasicAuth, retries: int = 3, delay: int = 5
) -> Optional[str]:
    for attempt in range(retries):
        try:
            response = requests.get(url, auth=auth)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.text  # Return XML data if successful
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    print(f"Failed to fetch data at {url} after {retries} attempts")
    return None


def get_prices(market_name: str, date_str: str) -> List[Price]:
    market = [market for market in MyMarkets if market.name == market_name][0]
    p_node = [p_node for p_node in MyPNodes if p_node.alias == market.p_node_alias][0]
    type = "da" if "da60" in market_name else "rt"

    request_info = {
        "url": f"https://webservices.iso-ne.com/api/v1.1/hourlylmp/{type}/final/day/{date_str}/location/{p_node.iso_id}",
        "auth": HTTPBasicAuth(
            username="jmillar@gridworks-consulting.com",
            password=Settings(
                _env_file=dotenv.find_dotenv()
            ).isone_api_pass.get_secret_value(),
        ),
    }

    xml_data = fetch_with_retry(request_info["url"], request_info["auth"])
    if xml_data is None:
        raise ValueError("No data?")
    else:
        tree = ET.ElementTree(ET.fromstring(xml_data))
        root = tree.getroot()
        namespace = {"ns": "http://WEBSERV.iso-ne.com"}

        prices = []

        for hourly_lmp in root.findall("ns:HourlyLmp", namespace):
            loc_id = hourly_lmp.find("ns:Location", namespace).attrib.get("LocId")
            if loc_id == p_node.iso_id:
                begin_date = hourly_lmp.find("ns:BeginDate", namespace).text
                lmp_total = float(hourly_lmp.find("ns:LmpTotal", namespace).text)
                begin_date_obj = datetime.strptime(begin_date, "%Y-%m-%dT%H:%M:%S.%f%z")
                slot_start_s = int(begin_date_obj.timestamp())
                prices.append(
                    Price(
                        market_slot_name=f"{market.name}.{slot_start_s}",
                        market_name=market.name,
                        slot_start_s=slot_start_s,
                        value=lmp_total,
                    )
                )
        return prices


def get_48h_day_ahead_forecast(start_time: pendulum.DateTime) -> HourlyPriceForecastSql:
    if start_time.minute != 0 or start_time.second != 0:
        raise ValueError("The start time must be rounded at the hour (0 min and 0 sec)")

    today = start_time.strftime("%Y%m%d")
    tomorrow = start_time.add(days=1).strftime("%Y%m%d")
    forecast_today = get_prices(
        market_name="e.da60.hw1.isone.ver.keene", date_str=today
    )
    forecast_tomorrow = get_prices(
        market_name="e.da60.hw1.isone.ver.keene", date_str=tomorrow
    )

    prices_today = [x.value for x in forecast_today]
    prices_tomorrow = [x.value for x in forecast_tomorrow]

    if start_time.hour <= 12:
        prices = (
            prices_today[start_time.hour :]
            + prices_today
            + prices_today[: start_time.hour]
        )
    else:
        prices = (
            prices_today[start_time.hour :]
            + prices_tomorrow
            + prices_tomorrow[: start_time.hour]
        )

    forecast = HourlyPriceForecastSql(
        price_uid="x",
        from_g_node_alias="hw1.isone.ps",
        channel_name="keene.48",
        start_unix_s=start_time.timestamp(),
        hour_starting_prices=prices,
        forecast_created_s=pendulum.now().timestamp(),
    )

    return forecast


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    # ORIGINAL USE
    # start_time = pendulum.datetime(2025,2,27,13,0,0)
    # forecast = get_48h_day_ahead_forecast(start_time)
    # plt.step(range(48), forecast.hour_starting_prices, where="post")
    # plt.show()
    # END

    start_time = pendulum.datetime(2023, 9, 30)

    all_da_prices, all_da_times = [], []
    all_rt_prices, all_rt_times = [], []
    while start_time < pendulum.datetime(2024, 4, 30):
        # while start_time < pendulum.datetime(2023, 10, 30):
        start_time = start_time.add(days=1)
        print(start_time)
        da_prices = get_prices(
            market_name="e.da60.hw1.isone.ver.keene",
            date_str=start_time.strftime("%Y%m%d"),
        )
        all_da_prices.extend([x.value for x in da_prices])
        all_da_times.extend([x.slot_start_s for x in da_prices])
        rt_prices = get_prices(
            market_name="e.rt60gate5.hw1.isone.ver.keene",
            date_str=start_time.strftime("%Y%m%d"),
        )
        all_rt_prices.extend([x.value for x in rt_prices])
        all_rt_times.extend([x.slot_start_s for x in rt_prices])
        if all_da_times != all_rt_times:
            break

    with open("winter_2023_2024_prices.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["time", "dayahead", "realtime"])
        for item1, item2, item3 in zip(all_da_times, all_da_prices, all_rt_prices):
            writer.writerow([item1, item2, item3])

    all_da_times = [
        pendulum.from_timestamp(x, tz="America/New_York") for x in all_rt_times
    ]
    plt.step(all_da_times, all_da_prices, where="post", label="Day ahead")
    plt.step(all_da_times, all_rt_prices, where="post", label="Real time")
    plt.legend()
    plt.show()
