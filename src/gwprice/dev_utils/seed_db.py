import os

import dotenv
from gwprice.codec import pyd_to_sql
from gwprice.config import Settings
from gwprice.enums import MarketCategory, MarketPriceUnit, MarketTypeName
from gwprice.models.forecast_methods import bulk_insert_forecast_methods
from gwprice.models.hourly_price_forecast_channels import (
    bulk_insert_channels,
)
from gwprice.models.markets import bulk_insert_markets
from gwprice.models.p_nodes import bulk_insert_p_nodes
from gwprice.models.prices import bulk_insert_prices
from gwprice.my_forecast_methods import MyForecastMethods
from gwprice.my_hourly_forecast_channels import MyForecastChannels
from gwprice.my_markets import MyMarkets
from gwprice.my_p_nodes import MyPNodes
from gwprice.property_format import MarketMinutes
from gwprice.type_helpers.hourly_price_csv import HourlyPriceCsv
from gwprice.type_helpers.price import Price
from gwprice.types import Market
from sqlalchemy import (
    create_engine,
)
from sqlalchemy.orm import sessionmaker

settings = Settings(_env_file=dotenv.find_dotenv())
engine = create_engine(settings.db_url.get_secret_value())
MySession = sessionmaker(bind=engine)
session = MySession()

bulk_insert_p_nodes(session, [pyd_to_sql(p_node) for p_node in MyPNodes])


bulk_insert_forecast_methods(
    session, [pyd_to_sql(forecast) for forecast in MyForecastMethods]
)


bulk_insert_markets(session, [pyd_to_sql(market) for market in MyMarkets])

bulk_insert_channels(session, [pyd_to_sql(channel) for channel in MyForecastChannels])


m = Market(
    name="e.rt60gate5.hw1.isone.ver.keene",
    market_type_name=MarketTypeName.rt60gate5,
    p_node_alias="hw1.isone.ver.keene",
    category=MarketCategory.Energy,
    unit=MarketPriceUnit.USDPerMWh,
)

folder_path = "input_data/electricity_prices/isone"
for file_name in os.listdir(folder_path):
    if file_name.endswith("csv"):
        file_path = os.path.join(folder_path, file_name)
        h = HourlyPriceCsv.from_csv(file_path)
        my_market_names = [market.name for market in MyMarkets]
        if h.market_name not in my_market_names:
            print(f"Not loading prices for {h.market_name} - not one of my markets")
        else:
            start_s = h.start_unix_s()
            slot_minutes = MarketMinutes[h.market_type()]

            prices = []
            for i in range(len(h.price_list)):
                slot_start = start_s + i * slot_minutes * 60
                prices.append(
                    Price(
                        market_slot_name=f"{h.market_name}.{slot_start}",
                        market_name=h.market_name,
                        slot_start_s=slot_start,
                        price=h.price_list[0],
                    )
                )

            sql_prices = [pyd_to_sql(price) for price in prices]
            print(f"Inserting prices for {h.market_name} from {file_name}")
            bulk_insert_prices(session, sql_prices)
