import json
import pendulum
from sqlalchemy.orm import Session

from gwprice.codec import sql_to_pyd
from gwprice.models import (
    ForecastMethodSql,
    HourlyPriceForecastChannelSql,
    MarketSql,
    PNodeSql,
)
from gwprice.my_forecast_methods import MyForecastMethods
from gwprice.my_hourly_forecast_channels import MyForecastChannels
from gwprice.my_markets import MyMarkets
from gwprice.my_p_nodes import MyPNodes



def rt_to_da_name(market_name: str) -> str:
    parts = market_name.split('.')
    # Check if the second part is 'rt60gate5' and replace it with 'da60'
    if len(parts) > 1 and parts[1] == "rt60gate5":
        parts[1] = "da60"
    return '.'.join(parts)


def isone_date_str(time_s: int, channel: HourlyPriceForecastChannelSql) -> str:
    dt = pendulum.from_timestamp(time_s, channel.market.p_node.tz)
    return dt.strftime("%Y%m%d")



def check_locals(db: Session):
    db_p_nodes = [sql_to_pyd(p) for p in db.query(PNodeSql).all()]

    same = True
    for p in MyPNodes:
        p_db = next((p_db for p_db in db_p_nodes if p_db.id == p.id), None)
        if p != p_db:
            same = False
            print(p)
            print(p_db)

    if not same:
        print("Update MyPNodes:")
        json.dumps([p.to_dict() for p in db_p_nodes])

    db_markets = [sql_to_pyd(m) for m in db.query(MarketSql).all()]
    same = True
    for m in MyMarkets:
        m_db = next((m_db for m_db in db_markets if m_db.name == m.name), None)
        if m != m_db:
            same = False
            print(m)
            print(m_db)

    if not same:
        print("Update MyMarkets:")
        json.dumps([m.to_dict() for m in db_markets])

    db_methods = [sql_to_pyd(m) for m in db.query(ForecastMethodSql).all()]
    same = True
    for m in MyForecastMethods:
        m_db = next((m_db for m_db in db_methods if m_db.alias == m.alias), None)
        if m != m_db:
            same = False
            print(m)
            print(m_db)

    if not same:
        print("Update ForecastMethods:")
        json.dumps([m.to_dict() for m in db_methods])

    db_channels = [sql_to_pyd(m) for m in db.query(HourlyPriceForecastChannelSql).all()]
    same = True
    for c in MyForecastChannels.values():
        c_db = next((c_db for c_db in db_channels if c_db.name == c.name), None)
        if c != c_db:
            same = False
            print(c)
            print(c_db)

    if not same:
        print("Update Channels:")
        json.dumps([c.to_dict() for c in db_channels])
