"""
Tests for enum energy.supply.type.000 from the GridWorks Type Registry.
"""

from gwprice.enums import EnergySupplyType


def test_energy_supply_type() -> None:
    assert set(EnergySupplyType.values()) == {
        "Unknown",
        "StandardOffer",
        "RealtimeLocalLmp",
    }

    assert EnergySupplyType.default() == EnergySupplyType.Unknown
    assert EnergySupplyType.enum_name() == "energy.supply.type"
    assert EnergySupplyType.enum_version() == "000"

    assert EnergySupplyType.version("Unknown") == "000"
    assert EnergySupplyType.version("StandardOffer") == "000"
    assert EnergySupplyType.version("RealtimeLocalLmp") == "000"

    for value in EnergySupplyType.values():
        symbol = EnergySupplyType.value_to_symbol(value)
        assert EnergySupplyType.symbol_to_value(symbol) == value
