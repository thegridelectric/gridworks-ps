"""Tests price.forecast.channel.list type, version 000"""

from gwprice.types import PriceForecastChannelList


def test_price_forecast_channel_list_generated() -> None:
    d = {
        "FromGNodeAlias": "hw1.isone.ps",
        "ChannelList": [
            {
                "Name": "keene.rt60.da1.48",
                "MarketName": "e.rt60gate5.d1.isone.ver.keene",
                "TotalHours": 48,
                "MethodAlias": "isoneexpress.da.web",
                "TypeName": "hourly.price.forecast.channel",
                "Version": "000",
            }
        ],
        "TypeName": "price.forecast.channel.list",
        "Version": "000",
    }

    assert PriceForecastChannelList.from_dict(d).to_dict() == d
