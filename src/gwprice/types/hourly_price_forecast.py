"""Type hourly.price.forecast, version 000"""

import json
from typing import Any, Dict, List, Literal

from gw.errors import GwTypeError
from gw.utils import recursively_pascal, snake_to_pascal
from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

from gwprice.types.hourly_price_forecast_channel import HourlyPriceForecastChannel
from gwprice.property_format import (
    LeftRightDot,
    UTCSeconds,
    UUID4Str,
)


class HourlyPriceForecast(BaseModel):
    from_g_node_alias: LeftRightDot
    channel: HourlyPriceForecastChannel
    start_unix_s: UTCSeconds
    prices: List[float]
    price_uid: UUID4Str
    type_name: Literal["hourly.price.forecast"] = "hourly.price.forecast"
    version: Literal["000"] = "000"

    model_config = ConfigDict(
        alias_generator=snake_to_pascal, frozen=True, populate_by_name=True, use_enum_values=True,
    )

    @field_validator("start_unix_s")
    @classmethod
    def check_start_unix_s(cls, v: int) -> int:
        """
        Axiom 1: StartUnixS must be at the top of the hour.
        """
        # Implement Axiom(s)
        return v

    @classmethod
    def from_dict(cls, d: dict) -> "HourlyPriceForecast":
        if not recursively_pascal(d):
                raise GwTypeError(f"dict is not recursively pascal case! {d}")
        try:
            t = cls(**d)
        except ValidationError as e:
            raise GwTypeError(f"Pydantic validation error: {e}") from e
        return t

    @classmethod
    def from_type(cls, b: bytes) -> "HourlyPriceForecast":
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
        d["Channel"] = self.channel.to_dict()
        return d

    def to_type(self) -> bytes:
        """
        Serialize to the hourly.price.forecast.000 representation designed to send in a message.
        """
        json_string = json.dumps(self.to_dict())
        return json_string.encode("utf-8")

    @classmethod
    def type_name_value(cls) -> str:
        return "hourly.price.forecast"
