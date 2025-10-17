from typing import Literal

from pydantic import model_validator
from typing_extensions import Self

from gwprice.asl.codec import AslType
from gwprice.asl.property_format import LeftRightDot, UTCMilliseconds


class Gw0RealtimePrice(AslType):
    from_g_node_alias: LeftRightDot # for now set to hw1.isone.me.keene.ps
    unix_ms: UTCMilliseconds # use integers for time
    lmp: float
    dist: float
    energy: float
    type_name: Literal["gw0.realtime.price"] = "gw0.realtime.price"

    @model_validator(mode='after')
    def check_axiom_1(self) -> Self:
        """Axiom 1: energy must be lmp + dist"""
        if self.lmp + self.dist != self.energy:
            raise ValueError("Axiom 1: energy must be lmp + dist")
        return self
