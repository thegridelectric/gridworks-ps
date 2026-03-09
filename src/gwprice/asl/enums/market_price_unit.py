from enum import auto

from gwprice.asl.enums.gw_str_enum import GwStrEnum


class MarketPriceUnit(GwStrEnum):
    """
    Price unit assigned to MarketMaker MarketType

    Enum market.price.unit version 000 in the GridWorks Type registry.

    Used by multiple Application Shared Languages (ASLs). For more information:
      - [ASLs](https://gridworks-type-registry.readthedocs.io/en/latest/)
      - [Global Authority](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#marketpriceunit)

    Values (with symbols in parens):
      - USDPerMWh (00000000)
    """

    USDPerMWh = auto()

    @classmethod
    def default(cls) -> "MarketPriceUnit":
        """
        Returns default value (in this case USDPerMWh)
        """
        return cls.USDPerMWh

    @classmethod
    def values(cls) -> list[str]:
        """
        Returns enum choices
        """
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        """
        The name in the GridWorks Type Registry (market.price.unit)
        """
        return "market.price.unit"

    @classmethod
    def enum_version(cls) -> str:
        """
        The version in the GridWorks Type Registry (000)
        """
        return "000"
