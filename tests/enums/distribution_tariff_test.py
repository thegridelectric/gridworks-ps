"""Tests for enum distribution.tariff.000"""
from gwprice.enums import DistributionTariff


def test_distribution_tariff() -> None:
    assert set(DistributionTariff.values()) == {
        "Unknown",
        "VersantA1StorageHeatTariff",
        "VersantATariff",
        "VersantA20Tariff",
    }

    assert DistributionTariff.default() == DistributionTariff.Unknown
