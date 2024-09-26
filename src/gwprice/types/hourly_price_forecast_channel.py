"""Type hourly.price.forecast.channel, version 000"""

import json
from typing import Any, Dict, Literal

from gw.errors import GwTypeError
from gw.utils import recursively_pascal, snake_to_pascal
from pydantic import BaseModel, ConfigDict, ValidationError, model_validator, PositiveInt
, StrictInt

from gwprice.enums import MarketCategory
from gwprice.enums import MarketPriceUnit
from gwprice.property_format import (
    LeftRightDot,
)


class HourlyPriceForecastChannel(BaseModel):
    """
    
    """
    name: LeftRightDot
    p_node_alias: LeftRightDot
    category: MarketCategory
    total_hours: PositiveInt
    method_alias: LeftRightDot
    unit: MarketPriceUnit
    type_name: Literal["hourly.price.forecast.channel"] = "hourly.price.forecast.channel"
    version: Literal["000"] = "000"

    model_config = ConfigDict(
        alias_generator=snake_to_pascal, frozen=True, populate_by_name=True,
    )

    @model_validator(mode="before")
    @classmethod
    def translate_enums(cls, data: dict) -> dict:
        if "CategoryGtEnumSymbol" in data:
            data["Category"] = MarketCategory.symbol_to_value(data["CategoryGtEnumSymbol"])
            del data["CategoryGtEnumSymbol"]
        if "UnitGtEnumSymbol" in data:
            data["Unit"] = MarketPriceUnit.symbol_to_value(data["UnitGtEnumSymbol"])
            del data["UnitGtEnumSymbol"]
        return data

    @classmethod
    def from_dict(cls, d: dict) -> "HourlyPriceForecastChannel":
        if not recursively_pascal(d):
                raise GwTypeError(f"dict is not recursively pascal case! {d}")
        try:
            t = cls(**d)
        except ValidationError as e:
            raise GwTypeError(f"Pydantic validation error: {e}") from e
        return t

    @classmethod
    def from_type(cls, b: bytes) -> "HourlyPriceForecastChannel":
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
        d["Unit"] = self.unit.value
        return d

    def to_type(self) -> bytes:
        """
        Serialize to the hourly.price.forecast.channel.000 representation designed to send in a message.
        """
        json_string = json.dumps(self.to_dict())
        return json_string.encode("utf-8")

    @classmethod
    def type_name_value(cls) -> str:
        return "hourly.price.forecast.channel"
