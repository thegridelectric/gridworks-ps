"""
Tests for enum market.category.000 from the GridWorks Type Registry.
"""

from gwprice.enums import MarketCategory


def test_market_category() -> None:
    assert set(MarketCategory.values()) == {
        "Energy",
        "Distribution",
        "Regulation",
    }

    assert MarketCategory.default() == MarketCategory.Energy
    assert MarketCategory.enum_name() == "market.category"
    assert MarketCategory.enum_version() == "000"

    assert MarketCategory.version("Energy") == "000"
    assert MarketCategory.version("Distribution") == "000"
    assert MarketCategory.version("Regulation") == "000"

    for value in MarketCategory.values():
        symbol = MarketCategory.value_to_symbol(value)
        assert MarketCategory.symbol_to_value(symbol) == value
