"""Tests market type, version 000"""

from gwprice.enums import MarketCategory, MarketPriceUnit, MarketTypeName
from gwprice.types import Market


def test_market_generated() -> None:
    d = {
        "Name": "e.rt60gate5.d1.isone.ver.keene",
        "MarketTypeName": "rt60gate5",
        "PNodeAlias": "d1.isone.ver.keene",
        "Category": "Energy",
        "Unit": "USDPerMWh",
        "TypeName": "market",
        "Version": "000",
    }

    assert Market.from_dict(d).to_dict() == d
