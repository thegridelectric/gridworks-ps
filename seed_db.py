import os

from gwprice.codec import pyd_to_sql
from gwprice.database import get_db
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
from gwprice.type_helpers.price import Price
from gwprice.types import HourlyPriceCsv
from sqlalchemy.orm import Session


def seed_database(db: Session, update_prices: bool = False):
    bulk_insert_p_nodes(db, [pyd_to_sql(p_node) for p_node in MyPNodes])
    bulk_insert_forecast_methods(
        db, [pyd_to_sql(forecast) for forecast in MyForecastMethods]
    )
    bulk_insert_markets(db, [pyd_to_sql(market) for market in MyMarkets])
    bulk_insert_channels(db, [pyd_to_sql(channel) for channel in MyForecastChannels])

    if update_prices:
        folder_path = "../../../input_data/electricity_prices/isone"
        for file_name in os.listdir(folder_path):
            if file_name.endswith("csv"):
                file_path = os.path.join(folder_path, file_name)
                h = HourlyPriceCsv.from_csv(file_path)
                my_market_names = [market.name for market in MyMarkets]
                if h.market_name not in my_market_names:
                    print(
                        f"Not loading prices for {h.market_name} - not one of my markets"
                    )
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
                                price=h.price_list[i],
                            )
                        )

                    sql_prices = [pyd_to_sql(price) for price in prices]
                    print(f"Inserting prices for {h.market_name} from {file_name}")
                    bulk_insert_prices(db, sql_prices)


if __name__ == "__main__":
    with next(get_db()) as db:
        seed_database(db)
