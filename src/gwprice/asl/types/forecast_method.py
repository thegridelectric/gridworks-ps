from typing import Literal, Optional

from gwprice.asl.codec import AslType
from gwprice.asl.enums import MarketCategory
from gwprice.asl.property_format import LeftRightDot


class ForecastMethod(AslType):
    alias: LeftRightDot
    category: Optional[MarketCategory] = None
    description: str
    type_name: Literal["forecast.method"] = "forecast.method"
    version: Literal["000"] = "000"
