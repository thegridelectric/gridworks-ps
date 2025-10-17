from enum import auto

from gwprice.asl.enums.gw_str_enum import GwStrEnum


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
    def values(cls) -> list[str]:
        """
        Returns enum choices
        """
        return [elt.value for elt in cls]

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