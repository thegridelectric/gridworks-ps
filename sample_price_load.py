import os

from gwprice.codec import pyd_to_sql
from gwprice.models.prices import bulk_insert_prices
from gwprice.my_forecast_methods import MyForecastMethods
from gwprice.my_markets import MyMarkets
from gwprice.type_helpers.hourly_price_csv import HourlyPriceCsv
from gwprice.type_helpers.price import Price

folder_path = "input_data/electricity_prices/isone"
import dotenv
from gwprice.config import Settings
from sqlalchemy import (
    create_engine,
)
from sqlalchemy.orm import sessionmaker

settings = Settings(_env_file=dotenv.find_dotenv())
engine = create_engine(settings.db_url.get_secret_value())
MySession = sessionmaker(bind=engine)
session = MySession()


file_path = "input_data/electricity_prices/isone/eprt__hw1.isone.ver.keene__2022.csv"

h = HourlyPriceCsv.from_csv(file_path)


prices = [Price(market_slot_name = f"{h.market_name}.{h.start_unix_s()}",
          market_name = h.market_name,
          slot_start_s=h.start_unix_s(),
          price=h.price_list[0])]

sql_prices = [pyd_to_sql(price) for price in prices]
bulk_insert_prices(session, sql_prices)

