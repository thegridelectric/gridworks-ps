"""Tests hourly.price.forecast.channel type, version 000"""

from gwprice.types import HourlyPriceForecastChannel


def test_hourly_price_forecast_channel_generated() -> None:
    d = {
        "Name": "keene.rt60.da1.48",
        "MarketName": "e.rt60gate5.d1.isone.ver.keene",
        "TotalHours": 48,
        "MethodAlias": "isoneexpress.da.web",
        "TypeName": "hourly.price.forecast.channel",
        "Version": "000",
    }

    assert HourlyPriceForecastChannel.from_dict(d).to_dict() == d
