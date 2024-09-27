"""Type hourly.price.forecast, version 000"""

from typing import List, Literal

from pydantic import field_validator, model_validator
from typing_extensions import Self

# from gwprice.my_hourly_forecast_channels import MyForecastChannels
from gwprice.property_format import (
    LeftRightDot,
    UTCSeconds,
    UUID4Str,
)
from gwprice.types.gw_base import GwBase


class HourlyPriceForecast(GwBase):
    from_g_node_alias: LeftRightDot
    channel_name: LeftRightDot
    start_unix_s: UTCSeconds
    hour_starting_prices: List[float]
    price_uid: UUID4Str
    forecast_created_s: UTCSeconds
    type_name: Literal["hourly.price.forecast"] = "hourly.price.forecast"
    version: Literal["000"] = "000"

    # @field_validator("channel_name")
    # @classmethod
    # def check_channel_name(cls, v: str) -> str:
    #     my_channel_names = [c.name for c in MyForecastChannels]
    #     if v not in my_channel_names:
    #         raise ValueError(f"channel {v} must be in {MyForecastChannels}")
    #     return v

    @field_validator("start_unix_s")
    @classmethod
    def check_start_unix_s(cls, v: int) -> int:
        """
        Axiom 1: StartUnixS must be at the top of the hour.
        """
        # Implement Axiom(s)
        return v

    @model_validator(mode="after")
    def check_axiom_2(self) -> Self:
        """
        Axiom 2: Forecast made before start.
        ForecastCreatedS must be before StartUnixS
        """
        # Implement check for axiom 2"
        return self
