"""Type market, version 000"""

from typing import Literal

from pydantic import model_validator
from typing_extensions import Self

from gwprice.enums import MarketCategory, MarketPriceUnit, MarketTypeName

# from gwprice.my_p_nodes import MyPNodes
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

    # @field_validator("p_node_alias")
    # @classmethod
    # def check_p_node_alias(cls, v: int) -> str:
    #     my_p_node_aliases = [p.alias for p in MyPNodes]
    #     if v not in my_p_node_aliases:
    #         raise ValueError(f"p_node {v} must be in {MyPNodes}")
    #     return v

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
        # Implement check for axiom "
        return self
