"""Type forecast.method, version 000"""

from typing import Literal, Optional

from gw.named_types import GwBase

from gwprice.enums import MarketCategory
from gwprice.property_format import LeftRightDot


class ForecastMethod(GwBase):
    alias: LeftRightDot
    category: Optional[MarketCategory] = None
    description: str
    type_name: Literal["forecast.method"] = "forecast.method"
    version: Literal["000"] = "000"
