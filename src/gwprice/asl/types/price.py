from typing import Literal

from pydantic import model_validator
from typing_extensions import Self

# from gwprice.my_markets import MyMarkets ... TODO: should be one of my markets?
from gwprice.asl.codec import AslType
from gwprice.asl.property_format import MarketName, MarketSlotName, UTCSeconds


class Price(AslType):
    market_slot_name: MarketSlotName
    market_name: MarketName
    slot_start_s: UTCSeconds
    value: float
    type_name: Literal["gw0.price"] = "gw0.price"


    @model_validator(mode="after")
    def name_consistency(self) -> Self:
        if self.market_slot_name != f"{self.market_name}.{self.slot_start_s}":
            raise ValueError(
                f"{self.market_slot_name} should be {self.market_name}.{self.slot_start_s} "
            )
        return self
