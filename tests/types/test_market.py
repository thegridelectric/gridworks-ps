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

    ######################################
    # Behavior on unknown enum values: sends to default
    ######################################

    d2 = dict(d, MarketTypeName="unknown_enum_thing")
    assert Market.from_dict(d2).market_type_name == MarketTypeName.default()

    d2 = dict(d, Category="unknown_enum_thing")
    assert Market.from_dict(d2).category == MarketCategory.default()

    d2 = dict(d, Unit="unknown_enum_thing")
    assert Market.from_dict(d2).unit == MarketPriceUnit.default()
