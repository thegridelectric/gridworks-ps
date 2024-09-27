"""Tests get.hourly.price.forecast.channel type, version 000"""

from gwprice.types import GetHourlyPriceForecastChannel


def test_get_hourly_price_forecast_channel_generated() -> None:
    d = {
        "FromGNodeAlias": "hw1.isone.me.versant.keene.beech",
        "ToGNodeAlias": "hw1.isone.ps",
        "MarketName": "e.rt60gate5.d1.isone.ver.keene",
        "TotalHours": 48,
        "MethodAlias": "isoneexpress.finalrt.hr.web",
        "TypeName": "get.hourly.price.forecast.channel",
        "Version": "000",
    }

    assert GetHourlyPriceForecastChannel.from_dict(d).to_dict() == d
