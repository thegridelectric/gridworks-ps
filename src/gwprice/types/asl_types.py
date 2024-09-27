"""List of all the types used by the actor."""

from typing import Dict, List, no_type_check

from gwprice.types.get_hourly_price_forecast_channel import (
    GetHourlyPriceForecastChannel,
)
from gwprice.types.gw_base import GwBase
from gwprice.types.hourly_price_forecast import HourlyPriceForecast
from gwprice.types.hourly_price_forecast_channel import HourlyPriceForecastChannel
from gwprice.types.market import Market
from gwprice.types.price_forecast_channel_list import PriceForecastChannelList

TypeByName: Dict[str, GwBase] = {}


@no_type_check
def type_makers() -> List[GwBase]:
    return [
        GetHourlyPriceForecastChannel,
        HourlyPriceForecast,
        HourlyPriceForecastChannel,
        Market,
        PriceForecastChannelList,
    ]


for maker in type_makers():
    TypeByName[maker.type_name] = maker


def version_by_type_name() -> Dict[str, str]:
    """
    Returns:
        Dict[str, str]: Keys are TypeNames, values are versions
    """

    v: Dict[str, str] = {
        "get.hourly.price.forecast.channel": "000",
        "hourly.price.forecast": "000",
        "hourly.price.forecast.channel": "000",
        "market": "000",
        "price.forecast.channel.list": "000",
    }

    return v


def status_by_versioned_type_name() -> Dict[str, str]:
    """
    Returns:
        Dict[str, str]: Keys are versioned TypeNames, values are type status
    """

    v: Dict[str, str] = {
        "get.hourly.price.forecast.channel.000": "Pending",
        "hourly.price.forecast.000": "Pending",
        "hourly.price.forecast.channel.000": "Pending",
        "market.000": "Pending",
        "price.forecast.channel.list.000": "Pending",
    }

    return v
