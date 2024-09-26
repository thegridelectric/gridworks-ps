"""Type get.hourly.price.forecast.channel, version 000"""

import json
from typing import Any, Dict, Literal

from gw.errors import GwTypeError
from gw.utils import recursively_pascal, snake_to_pascal
from pydantic import BaseModel, ConfigDict, ValidationError, model_validator, PositiveInt

from gwprice.enums import MarketCategory
from gwprice.property_format import (
    LeftRightDot,
)


class GetHourlyPriceForecastChannel(BaseModel):
    """
    Request to a price service for a forecast of distribution prices at a particular PNode
    """
    from_g_node_alias: LeftRightDot
    to_g_node_alias: LeftRightDot
    p_node_alias: LeftRightDot
    category: MarketCategory
    total_hours: PositiveInt
    method_alias: LeftRightDot
    type_name: Literal["get.hourly.price.forecast.channel"] = "get.hourly.price.forecast.channel"
    version: Literal["000"] = "000"

    model_config = ConfigDict(
        alias_generator=snake_to_pascal, frozen=True, populate_by_name=True, use_enum_values=True
    )

    @model_validator(mode="before")
    @classmethod
    def translate_enums(cls, data: dict) -> dict:
        if "CategoryGtEnumSymbol" in data:
            data["Category"] = MarketCategory.symbol_to_value(data["CategoryGtEnumSymbol"])
            del data["CategoryGtEnumSymbol"]
        return data

    @classmethod
    def from_dict(cls, d: dict) -> "GetHourlyPriceForecastChannel":
        if not recursively_pascal(d):
                raise GwTypeError(f"dict is not recursively pascal case! {d}")
        try:
            t = cls(**d)
        except ValidationError as e:
            raise GwTypeError(f"Pydantic validation error: {e}") from e
        return t

    @classmethod
    def from_type(cls, b: bytes) -> "GetHourlyPriceForecastChannel":
        try:
            d = json.loads(b)
        except TypeError as e:
            raise GwTypeError("Type must be string or bytes!") from e
        if not isinstance(d, dict):
            raise GwTypeError(f"Deserializing must result in dict!\n <{b}>")
        return cls.from_dict(d)

    def to_dict(self) -> Dict[str, Any]:
        """
        Handles lists of enums differently than model_dump
        """
        d = self.model_dump(exclude_none=True, by_alias=True)
        d["Category"] = self.category.value
        return d

    def to_type(self) -> bytes:
        """
        Serialize to the get.hourly.price.forecast.channel.000 representation designed to send in a message.
        """
        json_string = json.dumps(self.to_dict())
        return json_string.encode("utf-8")

    @classmethod
    def type_name_value(cls) -> str:
        return "get.hourly.price.forecast.channel"
