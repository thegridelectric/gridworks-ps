import time
import xml.etree.ElementTree as ET
from datetime import datetime
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

def get_current_lmp(market_name: str):
    market = [market for market in MyMarkets if market.name == market_name][0]
    p_node = [p_node for p_node in MyPNodes if p_node.alias == market.p_node_alias][0]

    request_info = {
        "url": f"https://webservices.iso-ne.com/api/v1.1/fiveminutelmp/current/location/{p_node.iso_id}",
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
        root = ET.fromstring(xml_data)
        namespace = {"ns": "http://WEBSERV.iso-ne.com"}
        lmp = float(root.find("ns:LmpTotal", namespaces=namespace).text)
        return lmp

def get_hourly_lmp(market_name: str, date_str: str) -> List[Price]:
    market = [market for market in MyMarkets if market.name == market_name][0]
    p_node = [p_node for p_node in MyPNodes if p_node.alias == market.p_node_alias][0]
    type = 'da' if 'da60' in market_name else 'rt'

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
        

def get_48h_day_ahead_forecast(start_time:pendulum.DateTime)->HourlyPriceForecastSql:
    if start_time.minute!=0 or start_time.second!=0:
        raise ValueError("The start time must be rounded at the hour (0 min and 0 sec)")
    today = start_time.strftime("%Y%m%d")
    tomorrow = start_time.add(days=1).strftime("%Y%m%d")
    forecast_today = get_hourly_lmp(market_name="e.da60.hw1.isone.4001", date_str=today)
    forecast_tomorrow = get_hourly_lmp(market_name="e.da60.hw1.isone.4001", date_str=tomorrow)
    prices_today = [x.value for x in forecast_today]
    prices_tomorrow = [x.value for x in forecast_tomorrow]
    if start_time.hour <= 12:
        prices = prices_today[start_time.hour:] + prices_today + prices_today[:start_time.hour]
    else:
        prices = prices_today[start_time.hour:] + prices_tomorrow + prices_tomorrow[:start_time.hour]
    forecast = HourlyPriceForecastSql(
        price_uid = 'x',
        from_g_node_alias = "hw1.isone.ps",
        channel_name = "keene.48",
        start_unix_s = start_time.in_timezone('America/New_York').timestamp(),
        hour_starting_prices = prices,
        forecast_created_s = pendulum.now().timestamp()
        )
    return forecast


if __name__ == '__main__':

    # Test current LMP
    start_time = pendulum.now(tz='America/New_York').add(hours=-10)
    start_time = pendulum.datetime(start_time.year, start_time.month, start_time.day, start_time.hour)
    price = get_current_lmp(market_name="e.rt60gate5.hw1.isone.ver.keene")
    print(f"Current LMP: {price}")

    # Test 48-hour day ahead forecast
    import matplotlib.pyplot as plt
    start_time = pendulum.now(tz='America/New_York').add(hours=1)
    start_time = pendulum.datetime(start_time.year, start_time.month, start_time.day, start_time.hour)
    forecast = get_48h_day_ahead_forecast(start_time)
    unix_times = [forecast.start_unix_s + i*3600 for i in range(48)]
    datetimes = [pendulum.from_timestamp(x) for x in unix_times]
    lmp_prices = forecast.hour_starting_prices
    dist_prices = [
        487.63 if x.hour in [7,8,9,10,11,16,17,18,19] and x.weekday() in [0,1,2,3,4]
        else 54.98 if x.hour in [12,13,14,15] and x.weekday() in [0,1,2,3,4]
        else 50.13
        for x in datetimes
    ]
    plt.step(datetimes, lmp_prices, where="post", label='LMP')
    plt.step(datetimes, dist_prices, where="post", label='Dist')
    plt.title('48 Hour Day Ahead Forecast')
    plt.legend()
    plt.show()