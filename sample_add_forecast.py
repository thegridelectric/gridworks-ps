import uuid

from gwprice.database import SessionLocal

db = SessionLocal()
import pendulum
from gwprice.codec import pyd_to_sql, sql_to_pyd
from gwprice.models import MarketSql, PriceSql  # Replace with your actual model
from gwprice.my_hourly_forecast_channels import MyForecastChannels
from gwprice.types import HourlyPriceForecast
from sqlalchemy import func

channel_name = "maine.perfect.48"
channel = next(
    (channel for channel in MyForecastChannels.values() if channel.name == channel_name), None
)

db.query(func.min(PriceSql.slot_start_s)).filter(
    PriceSql.market_name == channel.market_name
).scalar()

market = sql_to_pyd(
    db.query(MarketSql).filter(MarketSql.name == channel.market_name).first()
)

start_s = 1546318800
pendulum.from_timestamp(start_s)

prices = []
for i in range(channel.total_hours):
    slot_start_s = i * 3600 + start_s
    market_slot_name = f"{market.name}.{slot_start_s}"
    p = sql_to_pyd(
        db.query(PriceSql).filter(PriceSql.market_slot_name == market_slot_name).first()
    )
    if p is None:
        price = 10000
    else:
        price = p.value
    prices.append(price)


h = HourlyPriceForecast(
    from_g_node_alias="hw1.isone.ps",
    channel_name=channel.name,
    start_unix_s=1577854800,
    hour_starting_prices=prices,
    price_uid=uuid.uuid4(),
)

h_db = pyd_to_sql(h)
db.add(h_db)
db.commit()
db.close()
