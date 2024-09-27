"""Type hourly.price.forecast.channel, version 000"""

from typing import Literal

from pydantic import PositiveInt, field_validator

from gwprice.my_forecast_methods import MyForecastMethods
from gwprice.my_markets import MyMarkets
from gwprice.property_format import (
    LeftRightDot,
    MarketName,
)
from gwprice.types.gw_base import GwBase


class HourlyPriceForecastChannel(GwBase):
    name: LeftRightDot
    market_name: MarketName
    total_hours: PositiveInt
    method_alias: LeftRightDot
    type_name: Literal["hourly.price.forecast.channel"] = (
        "hourly.price.forecast.channel"
    )
    version: Literal["000"] = "000"

    @field_validator("market_name")
    @classmethod
    def check_market_name(cls, v: int) -> str:
        my_market_names = [market.name for market in MyMarkets]
        if v not in my_market_names:
            raise ValueError(f"market_name {v} must be in {MyMarkets}")
        return v

    @field_validator("method_alias")
    @classmethod
    def check_method_alias(cls, v: int) -> str:
        my_method_aliases = [method.alias for method in MyForecastMethods]
        if v not in my_method_aliases:
            raise ValueError(f"market_name {v} must be in {MyForecastMethods}")
        return v
