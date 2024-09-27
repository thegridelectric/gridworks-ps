"""Type get.hourly.price.forecast.channel, version 000"""

from typing import Literal

from pydantic import PositiveInt

from gwprice.property_format import (
    LeftRightDot,
    MarketName,
)
from gwprice.types.gw_base import GwBase


class GetHourlyPriceForecastChannel(GwBase):
    from_g_node_alias: LeftRightDot
    to_g_node_alias: LeftRightDot
    market_name: MarketName
    total_hours: PositiveInt
    method_alias: LeftRightDot
    type_name: Literal["get.hourly.price.forecast.channel"] = (
        "get.hourly.price.forecast.channel"
    )
    version: Literal["000"] = "000"
