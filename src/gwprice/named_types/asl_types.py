"""List of all the types used by the actor."""

from typing import Dict, List, no_type_check

from gw.named_types import GwBase

from gwprice.named_types.forecast_method import ForecastMethod
from gwprice.named_types.get_hourly_price_forecast_channel import (
    GetHourlyPriceForecastChannel,
)
from gwprice.named_types.hourly_price_csv import HourlyPriceCsv
from gwprice.named_types.hourly_price_forecast import HourlyPriceForecast
from gwprice.named_types.hourly_price_forecast_channel import HourlyPriceForecastChannel
from gwprice.named_types.market import Market
from gwprice.named_types.p_node import PNode
from gwprice.named_types.price_forecast_channel_list import PriceForecastChannelList

TypeByName: Dict[str, GwBase] = {}


@no_type_check
def type_makers() -> List[GwBase]:
    return [
        ForecastMethod,
        GetHourlyPriceForecastChannel,
        HourlyPriceCsv,
        HourlyPriceForecast,
        HourlyPriceForecastChannel,
        Market,
        PNode,
        PriceForecastChannelList,
    ]


for maker in type_makers():
    TypeByName[maker.type_name_value()] = maker


def version_by_type_name() -> Dict[str, str]:
    """
    Returns:
        Dict[str, str]: Keys are TypeNames, values are versions
    """

    v: Dict[str, str] = {
        "forecast.method": "000",
        "get.hourly.price.forecast.channel": "000",
        "hourly.price.csv": "000",
        "hourly.price.forecast": "000",
        "hourly.price.forecast.channel": "000",
        "market": "000",
        "p.node": "000",
        "price.forecast.channel.list": "000",
    }

    return v


def status_by_versioned_type_name() -> Dict[str, str]:
    """
    Returns:
        Dict[str, str]: Keys are versioned TypeNames, values are type status
    """

    v: Dict[str, str] = {
        "forecast.method.000": "Pending",
        "get.hourly.price.forecast.channel.000": "Pending",
        "hourly.price.csv.000": "Pending",
        "hourly.price.forecast.000": "Active",
        "hourly.price.forecast.channel.000": "Active",
        "market.000": "Active",
        "p.node.000": "Pending",
        "price.forecast.channel.list.000": "Pending",
    }

    return v
