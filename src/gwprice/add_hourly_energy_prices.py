import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Optional

import dotenv
import requests
from requests.auth import HTTPBasicAuth
from sqlalchemy.orm import Session

from gwprice.codec import pyd_to_sql
from gwprice.config import Settings
from gwprice.database import SessionLocal
from gwprice.enums import MarketTypeName
from gwprice.models.prices import bulk_insert_prices
from gwprice.my_markets import MyMarkets
from gwprice.my_p_nodes import MyPNodes
from gwprice.type_helpers import Price


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


def add_hourly_prices_for_day(db: Session, market_name: str, date_str: str) -> bool:
    """
    Returns False if it gets no prices 
    """
    market = next((market for market in MyMarkets if market.name == market_name), None)
    if market is None:
        raise Exception(f"No market with name {market_name} in MyMarkets")
    print(date_str)
    iso_mkt_type = "rt"
    if market.market_type_name == MarketTypeName.da60:
        iso_mkt_type = "da"
    elif market.market_type_name in {
        MarketTypeName.rt15gate5,
        MarketTypeName.rt30gate5,
        MarketTypeName.rt5gate5,
    }:
        raise Exception(f"{market.market_type_name} doesn't have hourly markets")
    p_node = next(
        (p_node for p_node in MyPNodes if p_node.alias == market.p_node_alias), None
    )

    request_info = {
        "url": f"https://webservices.iso-ne.com/api/v1.1/hourlylmp/{iso_mkt_type}/final/day/{date_str}/location/{p_node.iso_id}",
        "auth": HTTPBasicAuth(
            username="jmillar@gridworks-consulting.com",
            password=Settings(
                _env_file=dotenv.find_dotenv()
            ).isone_api_pass.get_secret_value(),
        ),
    }

    xml_data = fetch_with_retry(request_info["url"], request_info["auth"])
    if xml_data is None:
        return False
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

        db_prices = [pyd_to_sql(price) for price in prices]
        if db_prices:
            bulk_insert_prices(db, db_prices)
            return True
        return False


def generate_day_strings(year: int, month: int) -> list[str]:
    start_date = datetime(year, month, 1)
    next_month = start_date.replace(day=28) + timedelta(days=4)
    end_date = next_month - timedelta(days=next_month.day)
    return [
        (start_date + timedelta(days=i)).strftime("%Y%m%d")
        for i in range((end_date - start_date).days + 1)
    ]


def add_hourly_prices(market_name: str, year: int, month: Optional[int] = None) -> None:
    if year < 2017:
        raise ValueError("Pick a year after 2018")
    market = next((market for market in MyMarkets if market.name == market_name), None)
    if market is None:
        raise Exception(f"No market with name {market_name} in MyMarkets")
    print(f"Adding prices for {market}")
    db = SessionLocal()
    try:
        if month is None:  # If no month is specified, do the whole year
            for m in range(1, 13):
                day_strings = generate_day_strings(year, m)
                for date_str in day_strings:
                    add_hourly_prices_for_day(db, market_name, date_str)
        else:  # If a specific month is specified
            if month not in range(1, 13):
                raise ValueError("Please pick a month between 1 and 12")
            day_strings = generate_day_strings(year, month)
            for date_str in day_strings:
                add_hourly_prices_for_day(db, market_name, date_str)
    finally:
        db.close()
