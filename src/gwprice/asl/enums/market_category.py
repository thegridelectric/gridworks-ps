from enum import auto

from gwprice.asl.enums.gw_str_enum import GwStrEnum


class MarketCategory(GwStrEnum):
    """


    Enum market.category version 000 in the GridWorks Type registry.

    Used by multiple Application Shared Languages (ASLs). For more information:
      - [ASLs](https://gridworks-type-registry.readthedocs.io/en/latest/)
      - [Global Authority](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#marketcategory)

    Values (with symbols in parens):
      - Energy (00000000)
      - Distribution (33577a33)
      - Regulation (8d967d56)
    """

    Energy = auto()
    Distribution = auto()
    Regulation = auto()

    @classmethod
    def default(cls) -> "MarketCategory":
        """
        Returns default value (in this case Energy)
        """
        return cls.Energy

    @classmethod
    def values(cls) -> list[str]:
        """
        Returns enum choices
        """
        return [elt.value for elt in cls]


    @classmethod
    def enum_name(cls) -> str:
        """
        The name in the GridWorks Type Registry (market.category)
        """
        return "market.category"

    @classmethod
    def enum_version(cls) -> str:
        """
        The version in the GridWorks Type Registry (000)
        """
        return "000"
