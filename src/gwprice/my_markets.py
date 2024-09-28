from typing import List

from gwprice.enums import MarketCategory, MarketPriceUnit, MarketTypeName
from gwprice.types.market import Market

MyMarkets: List[Market] = [
    Market(
        name="e.rt60gate5.hw1.isone.ver.keene",
        market_type_name=MarketTypeName.rt60gate5,
        p_node_alias="hw1.isone.ver.keene",
        category=MarketCategory.Energy,
        unit=MarketPriceUnit.USDPerMWh,
    ),
    Market(
        name="d.rt60gate5.hw1.isone.ver.keene",
        market_type_name=MarketTypeName.rt60gate5,
        p_node_alias="hw1.isone.ver.keene",
        category=MarketCategory.Distribution,
        unit=MarketPriceUnit.USDPerMWh,
    ),
    Market(
        name="e.da60.hw1.isone.4001",
        market_type_name=MarketTypeName.da60,
        p_node_alias="hw1.isone.4001",
        category=MarketCategory.Energy,
        unit=MarketPriceUnit.USDPerMWh,
    ),
    Market(
        name="e.rt60gate5.hw1.isone.4001",
        market_type_name=MarketTypeName.rt60gate5,
        p_node_alias="hw1.isone.4001",
        category=MarketCategory.Energy,
        unit=MarketPriceUnit.USDPerMWh,
    ),
    Market(
        name="r.rt60gate5.hw1.isone",
        market_type_name=MarketTypeName.rt60gate5,
        p_node_alias="hw1.isone",
        category=MarketCategory.Regulation,
        unit=MarketPriceUnit.USDPerMWh,
    ),
]
