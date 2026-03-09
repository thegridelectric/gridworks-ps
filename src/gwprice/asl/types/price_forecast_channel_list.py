from typing import List, Literal

from gwprice.asl.codec import AslType
from gwprice.asl.property_format import (
    LeftRightDot,
)
from gwprice.asl.types.hourly_price_forecast_channel import HourlyPriceForecastChannel


class PriceForecastChannelList(AslType):
    from_g_node_alias: LeftRightDot
    channel_list: List[HourlyPriceForecastChannel]
    type_name: Literal["price.forecast.channel.list"] = "price.forecast.channel.list"
    version: Literal["000"] = "000"
