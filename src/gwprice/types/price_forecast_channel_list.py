"""Type price.forecast.channel.list, version 000"""

from typing import List, Literal

from gwprice.property_format import (
    LeftRightDot,
)
from gwprice.types.gw_base import GwBase
from gwprice.types.hourly_price_forecast_channel import HourlyPriceForecastChannel


class PriceForecastChannelList(GwBase):
    from_g_node_alias: LeftRightDot
    channel_list: List[HourlyPriceForecastChannel]
    type_name: Literal["price.forecast.channel.list"] = "price.forecast.channel.list"
    version: Literal["000"] = "000"
