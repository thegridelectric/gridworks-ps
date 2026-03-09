from enum import auto

from gwprice.asl.enums.gw_str_enum import GwStrEnum


class EnergySupplyType(GwStrEnum):
    """


    Enum energy.supply.type version 000 in the GridWorks Type registry.

    Used by multiple Application Shared Languages (ASLs). For more information:
      - [ASLs](https://gridworks-type-registry.readthedocs.io/en/latest/)
      - [Global Authority](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#energysupplytype)

    Values (with symbols in parens):
      - Unknown (00000000)
      - StandardOffer (cb18f937)
      - RealtimeLocalLmp (e9dc99a6)
    """

    Unknown = auto()
    StandardOffer = auto()
    RealtimeLocalLmp = auto()

    @classmethod
    def default(cls) -> "EnergySupplyType":
        """
        Returns default value (in this case Unknown)
        """
        return cls.Unknown

    @classmethod
    def values(cls) -> list[str]:
        """
        Returns enum choices
        """
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        """
        The name in the GridWorks Type Registry (energy.supply.type)
        """
        return "energy.supply.type"

    @classmethod
    def enum_version(cls) -> str:
        """
        The version in the GridWorks Type Registry (000)
        """
        return "000"
