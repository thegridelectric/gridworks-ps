"""
Tests for enum distribution.tariff.000 from the GridWorks Type Registry.
"""

from gwprice.enums import DistributionTariff


def test_distribution_tariff() -> None:
    assert set(DistributionTariff.values()) == {
        "Unknown",
        "VersantA1StorageHeatTariff",
        "VersantATariff",
        "VersantA20HeatTariff",
    }

    assert DistributionTariff.default() == DistributionTariff.Unknown
    assert DistributionTariff.enum_name() == "distribution.tariff"
    assert DistributionTariff.enum_version() == "000"

    assert DistributionTariff.version("Unknown") == "000"
    assert DistributionTariff.version("VersantA1StorageHeatTariff") == "000"
    assert DistributionTariff.version("VersantATariff") == "000"
    assert DistributionTariff.version("VersantA20HeatTariff") == "000"

    for value in DistributionTariff.values():
        symbol = DistributionTariff.value_to_symbol(value)
        assert DistributionTariff.symbol_to_value(symbol) == value
