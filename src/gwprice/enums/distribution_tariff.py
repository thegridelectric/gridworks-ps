from enum import auto
from typing import List, Optional

from gw.enums import GwStrEnum


class DistributionTariff(GwStrEnum):
    """
    Name of distribution tariff of local network company/utility

    Enum distribution.tariff version 000 in the GridWorks Type registry.

    Used by multiple Application Shared Languages (ASLs). For more information:
      - [ASLs](https://gridworks-type-registry.readthedocs.io/en/latest/)
      - [Global Authority](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#distributiontariff)

    Values (with symbols in parens):
      - Unknown (00000000)
      - VersantA1StorageHeatTariff (2127aba6): Versant is a utility serving customers in Maine, and
        in particular serves much of the area behind the Keene Rd Constraint in the [GridWorks
        Millinocket Demo](https://gridworks.readthedocs.io/en/latest/millinocket-demo.html#background).
        Alternately known as the 'Home Eco Rate With Bonus Meter, Time-of-Use.' Look for rate
        A1 in Versant [rate schedules](https://www.versantpower.com/residential/rates/rates-schedules/);
        details are also available [here](https://drive.google.com/drive/u/0/folders/1mhIeNj2JWVyIJrQnSHmBDOkBpNnRRVKB).
        More: Service under this rate will be available to residential customers with thermal
        energy storage devices, electric battery storage devices, and/or vehicle chargers who
        agree to install a second metered point of delivery. The customer will be subject to
        inspections to ensure that the thermal storage device, electric battery storage device,
        and electric vehicle charger(s) are sized appropriately for residential use. If the
        thermal storage device, electric battery storage device, and electric vehicle charger(s)
        do not pass Company inspection, then the service will be denied. Service will be single-phase,
        alternating current, 60 hertz, at one standard secondary distribution voltage. Customers
        taking service under this rate schedule are responsible for paying both Distribution
        Service and Stranded Cost. See attached csv for instantiation of this rate as an 8760. [More Info](https://github.com/thegridelectric/gridworks-ps/blob/dev/input_data/electricity_prices/isone/distp__w.isone.stetson__2022__gw.me.versant.a1.res.ets.csv).
      - VersantATariff (ea5c675a): Versant is a utility serving customers in Maine, and in particular
        serves much of the area behind the Keene Rd Constraint in the [GridWorks Millinocket
        Demo](https://gridworks.readthedocs.io/en/latest/millinocket-demo.html#background).
        The A Tariff is their standard residential tariff. Look for rate A in Versant [rate
        schedules](https://www.versantpower.com/residential/rates/rates-schedules/)
      - VersantA20HeatTariff (54aec3a7): Versant is a utility serving customers in Maine, and in
        particular serves much of the area behind the Keene Rd Constraint in the [GridWorks
        Millinocket Demo](https://gridworks.readthedocs.io/en/latest/millinocket-demo.html#background).
        This is an alternative tariff available for electric heat.
    """

    Unknown = auto()
    VersantA1StorageHeatTariff = auto()
    VersantATariff = auto()
    VersantA20HeatTariff = auto()

    @classmethod
    def default(cls) -> "DistributionTariff":
        """
        Returns default value (in this case Unknown)
        """
        return cls.Unknown

    @classmethod
    def values(cls) -> List[str]:
        """
        Returns enum choices
        """
        return [elt.value for elt in cls]

    @classmethod
    def version(cls, value: Optional[str] = None) -> str:
        """
        Returns the version of the class (default) used by this package or the
        version of a candidate enum value (always less than or equal to the version
        of the class)

        Args:
            value (Optional[str]): None (for version of the Enum itself) or
            the candidate enum value.

        Raises:
            ValueError: If the value is not one of the enum values.

        Returns:
            str: The version of the enum used by this code (if given no
            value) OR the earliest version of the enum containing the value.
        """
        if value is None:
            return "000"
        if not isinstance(value, str):
            raise ValueError("This method applies to strings, not enums")
        if value not in value_to_version.keys():
            raise ValueError(f"Unknown enum value: {value}")
        return value_to_version[value]

    @classmethod
    def enum_name(cls) -> str:
        """
        The name in the GridWorks Type Registry (distribution.tariff)
        """
        return "distribution.tariff"

    @classmethod
    def enum_version(cls) -> str:
        """
        The version in the GridWorks Type Registry (000)
        """
        return "000"

    @classmethod
    def symbol_to_value(cls, symbol: str) -> str:
        """
        Given the symbol sent in a serialized message, returns the encoded enum.

        Args:
            symbol (str): The candidate symbol.

        Returns:
            str: The encoded value associated to that symbol. If the symbol is not
            recognized - which could happen if the actor making the symbol is using
            a later version of this enum, returns the default value of "Unknown".
        """
        if symbol not in symbol_to_value.keys():
            return cls.default().value
        return symbol_to_value[symbol]

    @classmethod
    def value_to_symbol(cls, value: str) -> str:
        """
        Provides the encoding symbol for a DistributionTariff enum to send in seriliazed messages.

        Args:
            symbol (str): The candidate value.

        Returns:
            str: The symbol encoding that value. If the value is not recognized -
            which could happen if the actor making the message used a later version
            of this enum than the actor decoding the message, returns the default
            symbol of "00000000".
        """
        if value not in value_to_symbol.keys():
            return value_to_symbol[cls.default().value]
        return value_to_symbol[value]

    @classmethod
    def symbols(cls) -> List[str]:
        """
        Returns a list of the enum symbols
        """
        return [
            "00000000",
            "2127aba6",
            "ea5c675a",
            "54aec3a7",
        ]


symbol_to_value = {
    "00000000": "Unknown",
    "2127aba6": "VersantA1StorageHeatTariff",
    "ea5c675a": "VersantATariff",
    "54aec3a7": "VersantA20HeatTariff",
}

value_to_symbol = {value: key for key, value in symbol_to_value.items()}

value_to_version = {
    "Unknown": "000",
    "VersantA1StorageHeatTariff": "000",
    "VersantATariff": "000",
    "VersantA20HeatTariff": "000",
}
