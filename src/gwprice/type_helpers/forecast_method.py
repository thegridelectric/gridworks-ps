from gwprice.enums import MarketCategory
from gwprice.property_format import LeftRightDot
from gwprice.types import GwBase


class ForecastMethod(GwBase):
    alias: LeftRightDot
    category: MarketCategory
    description: str
