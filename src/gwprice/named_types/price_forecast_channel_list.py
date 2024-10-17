"""Type price.forecast.channel.list, version 000"""

from typing import List, Literal

from gw.named_types import GwBase

from gwprice.named_types.hourly_price_forecast_channel import HourlyPriceForecastChannel
from gwprice.property_format import (
    LeftRightDot,
)


class PriceForecastChannelList(GwBase):
    from_g_node_alias: LeftRightDot
    channel_list: List[HourlyPriceForecastChannel]
    type_name: Literal["price.forecast.channel.list"] = "price.forecast.channel.list"
    version: Literal["000"] = "000"
