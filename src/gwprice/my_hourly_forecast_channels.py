from typing import Dict

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
    {
        "TypeName": "hourly.price.forecast.channel",
        "Version": "000",
        "Name": "maine.perfect.48",
        "MarketName": "e.rt60gate5.hw1.isone.4001",
        "TotalHours": 48,
        "MethodAlias": "isoneexpress.finalrt.hr.web",
    },
]
MyForecastChannels: Dict[str, HourlyPriceForecastChannel] = {
    d["Name"]: HourlyPriceForecastChannel.from_dict(d) for d in MyChannelDicts
}