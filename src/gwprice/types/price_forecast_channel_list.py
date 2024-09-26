"""Type price.forecast.channel.list, version 000"""

import json
from typing import Any, Dict, List, Literal

from gw.errors import GwTypeError
from gw.utils import recursively_pascal, snake_to_pascal
from pydantic import BaseModel, ConfigDict, ValidationError

from gwprice.types.hourly_price_forecast_channel import HourlyPriceForecastChannel
from gwprice.property_format import (
    LeftRightDot,
)


class PriceForecastChannelList(BaseModel):
    """
    
    """
    from_g_node_alias: LeftRightDot
    channel_list: List[HourlyPriceForecastChannel]
    type_name: Literal["price.forecast.channel.list"] = "price.forecast.channel.list"
    version: Literal["000"] = "000"

    model_config = ConfigDict(
        alias_generator=snake_to_pascal, frozen=True, populate_by_name=True,
    )

    @classmethod
    def from_dict(cls, d: dict) -> "PriceForecastChannelList":
        if not recursively_pascal(d):
                raise GwTypeError(f"dict is not recursively pascal case! {d}")
        try:
            t = cls(**d)
        except ValidationError as e:
            raise GwTypeError(f"Pydantic validation error: {e}") from e
        return t

    @classmethod
    def from_type(cls, b: bytes) -> "PriceForecastChannelList":
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
        d["ChannelList"] = [elt.to_dict() for elt in self.channel_list]
        return d

    def to_type(self) -> bytes:
        """
        Serialize to the price.forecast.channel.list.000 representation designed to send in a message.
        """
        json_string = json.dumps(self.to_dict())
        return json_string.encode("utf-8")

    @classmethod
    def type_name_value(cls) -> str:
        return "price.forecast.channel.list"
