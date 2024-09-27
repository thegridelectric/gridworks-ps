from typing import List

from gwprice.enums import MarketCategory, MarketPriceUnit, MarketTypeName
from gwprice.types.market import Market

MyMarkets: List[Market] = [
    Market(
        name="e.rt60gate5.d1.isone.ver.keene",
        market_type_name=MarketTypeName.rt60gate5,
        p_node_alias="d1.isone.ver.keene",
        category=MarketCategory.Energy,
        unit=MarketPriceUnit.USDPerMWh,
    ),
    Market(
        name="d.rt60gate5.d1.isone.ver.keene",
        market_type_name=MarketTypeName.rt60gate5,
        p_node_alias="d1.isone.ver.keene",
        category=MarketCategory.Distribution,
        unit=MarketPriceUnit.USDPerMWh,
    ),
]
