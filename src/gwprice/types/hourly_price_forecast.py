"""Type hourly.price.forecast, version 000"""

from typing import List, Literal, Optional

from pydantic import field_validator, model_validator
from typing_extensions import Self

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
    forecast_created_s: Optional[UTCSeconds] = None
    type_name: Literal["hourly.price.forecast"] = "hourly.price.forecast"
    version: Literal["000"] = "000"

    @field_validator("start_unix_s")
    @classmethod
    def check_start_unix_s(cls, v: int) -> int:
        """
        Axiom 1: StartUnixS must be at the top of the hour.
        """
        if v % 3600 != 0:
            raise ValueError(f"{v} is not at the top of the hour!")
        return v

    @model_validator(mode="after")
    def check_axiom_2(self) -> Self:
        """
        Axiom 2: Forecast made before start.
        If it exists, ForecastCreatedS must be before StartUnixS
        """
        if self.forecast_created_s:
            if self.forecast_created_s >= self.start_unix_s:
                raise ValueError(
                    "If ForecastCreatedS exists it must be smaller than StartUnixS!"
                )
        return self
