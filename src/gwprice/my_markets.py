from typing import List

from gwprice.types.market import Market

MyMarketDicts = [
    {
        "TypeName": "market",
        "Version": "000",
        "Name": "e.rt60gate5.hw1.isone.ver.keene.stetson",
        "MarketTypeName": "rt60gate5",
        "PNodeAlias": "hw1.isone.ver.keene.stetson",
        "Category": "Energy",
        "Unit": "USDPerMWh",
    },
    {
        "TypeName": "market",
        "Version": "000",
        "Name": "e.rt60gate5.hw1.isone.ver.keene",
        "MarketTypeName": "rt60gate5",
        "PNodeAlias": "hw1.isone.ver.keene",
        "Category": "Energy",
        "Unit": "USDPerMWh",
    },
    {
        "TypeName": "market",
        "Version": "000",
        "Name": "d.rt60gate5.hw1.isone.ver.keene",
        "MarketTypeName": "rt60gate5",
        "PNodeAlias": "hw1.isone.ver.keene",
        "Category": "Distribution",
        "Unit": "USDPerMWh",
    },
    {
        "TypeName": "market",
        "Version": "000",
        "Name": "e.da60.hw1.isone.ver.keene",
        "MarketTypeName": "da60",
        "PNodeAlias": "hw1.isone.ver.keene",
        "Category": "Energy",
        "Unit": "USDPerMWh",
    },
    {
        "TypeName": "market",
        "Version": "000",
        "Name": "e.da60.hw1.isone.4001",
        "MarketTypeName": "da60",
        "PNodeAlias": "hw1.isone.4001",
        "Category": "Energy",
        "Unit": "USDPerMWh",
    },
    {
        "TypeName": "market",
        "Version": "000",
        "Name": "e.rt60gate5.hw1.isone.4001",
        "MarketTypeName": "rt60gate5",
        "PNodeAlias": "hw1.isone.4001",
        "Category": "Energy",
        "Unit": "USDPerMWh",
    },
    {
        "TypeName": "market",
        "Version": "000",
        "Name": "r.rt60gate5.hw1.isone",
        "MarketTypeName": "rt60gate5",
        "PNodeAlias": "hw1.isone",
        "Category": "Regulation",
        "Unit": "USDPerMWh",
    },
    {
        "TypeName": "market",
        "Version": "000",
        "Name": "e.rt60gate5.hw1.isone.4007",
        "MarketTypeName": "rt60gate5",
        "PNodeAlias": "hw1.isone.4007",
        "Category": "Energy",
        "Unit": "USDPerMWh",
    },
    {
        "TypeName": "market",
        "Version": "000",
        "Name": "e.da60.hw1.isone.4007",
        "MarketTypeName": "da60",
        "PNodeAlias": "hw1.isone.4007",
        "Category": "Energy",
        "Unit": "USDPerMWh",
    },

]

MyMarkets: List[Market] = [Market.from_dict(d) for d in MyMarketDicts]
