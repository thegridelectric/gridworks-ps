import dotenv
from gwprice.codec import pyd_to_sql
from gwprice.config import Settings
from gwprice.models.forecast_methods import bulk_insert_forecast_methods
from gwprice.models.hourly_price_forecast_channels import (
    bulk_insert_channels,
)
from gwprice.models.markets import bulk_insert_markets
from gwprice.models.p_nodes import bulk_insert_p_nodes
from gwprice.my_forecast_methods import MyForecastMethods
from gwprice.my_hourly_forecast_channels import MyForecastChannels
from gwprice.my_markets import MyMarkets
from gwprice.my_p_nodes import MyPNodes
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


from gwprice.types import Market
from gwprice.enums import MarketCategory, MarketPriceUnit, MarketTypeName

m = Market(
        name="e.rt60gate5.hw1.isone.ver.keene",
        market_type_name=MarketTypeName.rt60gate5,
        p_node_alias="hw1.isone.ver.keene",
        category=MarketCategory.Energy,
        unit=MarketPriceUnit.USDPerMWh,
    )