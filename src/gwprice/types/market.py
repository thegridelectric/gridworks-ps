"""Type market, version 000"""

from typing import Literal

from pydantic import model_validator
from typing_extensions import Self

from gwprice.enums import MarketCategory, MarketPriceUnit, MarketTypeName
from gwprice.property_format import (
    LeftRightDot,
    MarketName,
)
from gwprice.types.gw_base import GwBase


class Market(GwBase):
    name: MarketName
    market_type_name: MarketTypeName
    p_node_alias: LeftRightDot
    category: MarketCategory
    unit: MarketPriceUnit
    type_name: Literal["market"] = "market"
    version: Literal["000"] = "000"

    @model_validator(mode="after")
    def check_axiom_1(self) -> Self:
        """
        Axiom : Name Derived from MarketTypeName, PNodeAlias and Category.
        Name = f"x.{MarketTypeName}.{PNode}" where x = e if category is energy, d if distribution, r if regulation.
        """
        suffix = f"{self.market_type_name}.{self.p_node_alias}"
        name_parts = self.name.split(".")
        remainder = ".".join(name_parts[1:])
        if suffix != remainder:
            raise ValueError(f"name {self.name} does not match {remainder}!")
        category_shorthand = name_parts[0]
        if (
            (self.category == MarketCategory.Energy and category_shorthand != "e")
            or (
                self.category == MarketCategory.Distribution
                and category_shorthand != "d"
            )
            or (
                self.category == MarketCategory.Regulation and category_shorthand != "r"
            )
        ):
            raise ValueError(f"name {self.name} does not match {self.category}")

        return self
