from pydantic import field_validator, model_validator
from typing_extensions import Self

from gwprice.my_markets import MyMarkets
from gwprice.property_format import MarketName, MarketSlotName, UTCSeconds
from gwprice.types import GwBase


class Price(GwBase):
    market_slot_name: MarketSlotName
    market_name: MarketName
    slot_start_s: UTCSeconds
    value: float

    @field_validator("market_slot_name")
    @classmethod
    def check_market_slot_name(cls, v: int) -> str:
        x = v.split(".")
        market_name = ".".join(v.split(".")[:-1])
        my_market_names = [market.name for market in MyMarkets]
        if market_name not in my_market_names:
            raise ValueError(f"market_name {market_name} must be in {my_market_names}")
        return v

    @model_validator(mode="after")
    def name_consistency(self) -> Self:
        if self.market_slot_name != f"{self.market_name}.{self.slot_start_s}":
            raise ValueError(
                f"{self.market_slot_name} should be {self.market_name}.{self.slot_start_s} "
            )
        return self
