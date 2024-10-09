import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Optional, List
import pendulum

import dotenv
import requests
from requests.auth import HTTPBasicAuth
from sqlalchemy.orm import Session

from gwprice.codec import pyd_to_sql
from gwprice.config import Settings
from gwprice.database import SessionLocal
from gwprice.enums import MarketTypeName
from gwprice.my_markets import MyMarkets
from gwprice.my_p_nodes import MyPNodes
from gwprice.type_helpers import Price
from gwprice.models import HourlyPriceForecastSql


def fetch_with_retry(url: str, auth: HTTPBasicAuth, retries: int = 3, delay: int = 5) -> Optional[str]:
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


def get_day_ahead_prices(market_name: str, date_str: str) -> List[Price]:

    market = [market for market in MyMarkets if market.name == market_name][0]
    p_node = [p_node for p_node in MyPNodes if p_node.alias == market.p_node_alias][0]

    request_info = {
        "url": f"https://webservices.iso-ne.com/api/v1.1/hourlylmp/da/final/day/{date_str}/location/{p_node.iso_id}",
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
        

def get_48h_day_ahead_forecast(start_time:pendulum.DateTime, market_name:str)->HourlyPriceForecastSql:

    if start_time.minute!=0 or start_time.second!=0:
        raise ValueError("The start time must be rounded at the hour (0 min and 0 sec)")

    today = start_time.strftime("%Y%m%d")
    tomorrow = start_time.add(days=1).strftime("%Y%m%d")
    forecast_today = get_day_ahead_prices(market_name, today)
    forecast_tomorrow = get_day_ahead_prices(market_name, tomorrow)

    prices_today = [x.value for x in forecast_today]
    prices_tomorrow = [x.value for x in forecast_tomorrow]

    if start_time.hour <= 12:
        prices = prices_today[start_time.hour:] + prices_today + prices_today[:start_time.hour]
    else:
        prices = prices_today[start_time.hour:] + prices_tomorrow + prices_tomorrow[:start_time.hour]

    forecast = HourlyPriceForecastSql(
        price_uid = 'a',
        from_g_node_alias = 'a',
        channel_name = 'a',
        start_unix_s = start_time.timestamp(),
        hour_starting_prices = prices,
        forecast_created_s = pendulum.now().timestamp()
        )

    return forecast


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    start_time = pendulum.datetime(2024,10,1,12,0,0)
    forecast = get_48h_day_ahead_forecast(start_time, market_name="e.da60.hw1.isone.ver.keene")
    plt.step(range(48), forecast.hour_starting_prices, where="post")
    plt.show()

    