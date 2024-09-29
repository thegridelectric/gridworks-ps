from typing import List

from gwprice.types.hourly_price_forecast_channel import HourlyPriceForecastChannel

MyForecastChannels: List[HourlyPriceForecastChannel] = [
    HourlyPriceForecastChannel(
        name="keene.48",
        market_name="e.rt60gate5.hw1.isone.ver.keene",
        total_hours=48,
        method_alias="basic.da",
    ),
    HourlyPriceForecastChannel(
        name="keene.rt60.da1.48",
        market_name="e.rt60gate5.hw1.isone.ver.keene",
        total_hours=48,
        method_alias="isoneexpress.da.web",
    ),
    HourlyPriceForecastChannel(
        name="keene.perfect.48",
        market_name="e.rt60gate5.hw1.isone.ver.keene",
        total_hours=48,
        method_alias="isoneexpress.finalrt.hr.web",
    ),
]
