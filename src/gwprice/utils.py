import json

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
    for c in MyForecastChannels:
        c_db = next((c_db for c_db in db_channels if c_db.name == c.name), None)
        if c != c_db:
            same = False
            print(c)
            print(c_db)

    if not same:
        print("Update Channels:")
        json.dumps([c.to_dict() for c in db_channels])
