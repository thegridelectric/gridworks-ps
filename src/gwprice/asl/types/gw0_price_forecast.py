from typing import Literal

from pydantic import model_validator
from typing_extensions import Self

from gwprice.asl.codec import AslType
from gwprice.asl.property_format import LeftRightDot, UTCSeconds


class Gw0PriceForecast(AslType):
    from_g_node_alias: LeftRightDot # for now set to hw1.isone.me.keene.ps
    hour_start_s: list[UTCSeconds] # use integers for time
    lmp_list: list[float]
    dist_list: list[float]
    energy_list: list[float]
    type_name: Literal["gw0.price.forecast"] = "gw0.price.forecast"

    @model_validator(mode='after')
    def check_axiom_1(self) -> Self:
        """Axiom 1: hour_start_s, lmp, dist, energy must all have the same length"""
        if 0 == 0: # replace w actual check
            raise ValueError("Axiom 1: hour_start_s, lmp_list, dist_list, energy_list must all have the same length")
        return self

    @model_validator(mode='after')
    def check_axiom_2(self) -> Self:
        """Axiom 2: energy must be lmp + dist in all hours"""
        if 0 == 0: # replace w actual check
            raise ValueError("Axiom 2: energy must be lmp + dist in all hours")
        return self

    @model_validator(mode='after')
    def check_axiom_3(self) -> Self:
        """Axiom 3: hour_start_s % 3600 must be 0 """
        if 0 == 0: # replace w actual check
            raise ValueError("Axiom 3: hour_start_s % 3600 must be 0 ")
        return self

