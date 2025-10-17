from typing import Literal

from pydantic import PositiveInt

from gwprice.asl.codec import AslType
from gwprice.asl.property_format import (
    LeftRightDot,
    MarketName,
)


class HourlyPriceForecastChannel(AslType):
    name: LeftRightDot
    market_name: MarketName
    total_hours: PositiveInt
    method_alias: LeftRightDot
    type_name: Literal["hourly.price.forecast.channel"] = (
        "hourly.price.forecast.channel"
    )
    version: Literal["000"] = "000"

    # @field_validator("market_name")
    # @classmethod
    # def check_market_name(cls, v: int) -> str:
    #     my_market_names = [market.name for market in MyMarkets]
    #     if v not in my_market_names:
    #         raise ValueError(f"market_name {v} must be in {MyMarkets}")
    #     return v

    # @field_validator("method_alias")
    # @classmethod
    # def check_method_alias(cls, v: int) -> str:
    #     my_method_aliases = [method.alias for method in MyForecastMethods]
    #     if v not in my_method_aliases:
    #         raise ValueError(f"market_name {v} must be in {MyForecastMethods}")
    #     return v
