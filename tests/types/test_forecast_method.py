"""Tests forecast.method type, version 000"""

from gwprice.enums import MarketCategory
from gwprice.types import ForecastMethod


def test_forecast_method_generated() -> None:
    d = {
        "Alias": "basic.da",
        "Category": "Energy",
        "Description": "Use DA prices for today, and once tomorrow's prices are available (typically between noon and 1 America/NY) use those prices for tomorrow. In either case, repeat the last day for the remaining hours.",
        "TypeName": "forecast.method",
        "Version": "000",
    }

    assert ForecastMethod.from_dict(d).to_dict() == d

    ######################################
    # Behavior on unknown enum values: sends to default
    ######################################

    d2 = dict(d, Category="unknown_enum_thing")
    assert ForecastMethod.from_dict(d2).category == MarketCategory.default()
