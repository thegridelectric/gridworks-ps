from typing import List

from gwprice.types.hourly_price_forecast_channel import HourlyPriceForecastChannel

MyChannelDicts = [
    {
        "TypeName": "hourly.price.forecast.channel",
        "Version": "000",
        "Name": "keene.48",
        "MarketName": "e.rt60gate5.hw1.isone.ver.keene",
        "TotalHours": 48,
        "MethodAlias": "basic.da",
    },
    {
        "TypeName": "hourly.price.forecast.channel",
        "Version": "000",
        "Name": "keene.rt60.da1.48",
        "MarketName": "e.rt60gate5.hw1.isone.ver.keene",
        "TotalHours": 48,
        "MethodAlias": "isoneexpress.da.web",
    },
    {
        "TypeName": "hourly.price.forecast.channel",
        "Version": "000",
        "Name": "keene.perfect.48",
        "MarketName": "e.rt60gate5.hw1.isone.ver.keene",
        "TotalHours": 48,
        "MethodAlias": "isoneexpress.finalrt.hr.web",
    },
]
MyForecastChannels: List[HourlyPriceForecastChannel] = [
    HourlyPriceForecastChannel.from_dict(d) for d in MyChannelDicts
]
