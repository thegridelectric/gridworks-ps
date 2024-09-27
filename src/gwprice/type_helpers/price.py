from pydantic import field_validator

from gwprice.my_markets import MyMarkets
from gwprice.property_format import MarketSlotName
from gwprice.types import GwBase


class Price(GwBase):
    market_slot_name: MarketSlotName
    price: float

    @field_validator("market_slot_name")
    @classmethod
    def check_market_slot_name(cls, v: int) -> str:
        x = v.split(".")
        market_name = f"{x[0]}.{x[1]}"
        my_market_names = [market.name for market in MyMarkets]
        if market_name not in my_market_names:
            raise ValueError(f"market_name {market_name} must be in {MyMarkets}")
        return v
