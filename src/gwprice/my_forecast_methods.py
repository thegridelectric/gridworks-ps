from typing import List

from gwprice.enums import MarketCategory
from gwprice.type_helpers.forecast_method import ForecastMethod

MyForecastMethods: List[ForecastMethod] = [
    ForecastMethod(
        alias="isoneexpress.finalrt.hr.web",
        category=MarketCategory.Energy,
        description="Final hourly realtime energy prices from " "isone isoexpress",
    ),
    ForecastMethod(
        alias="isoneexpress.da.web",
        category=MarketCategory.Energy,
        description="Hourly Day Ahead prices from isoexpress",
    ),
    ForecastMethod(
        alias="gw.da.predicted.rolling4wks.alpha",
        category=MarketCategory.Energy,
        description="Prediction of next period's LMP (electricity price) "
        "based on next period's day ahead and this period's "
        "real-time price done on a rolling 4 weeks continuously "
        "updating prediction parameters",
    ),
    ForecastMethod(
        alias="gw.pathways.alpha",
        category=MarketCategory.Energy,
        description="Prediction of next period's LMP (electricity price) based "
        "on next period's day ahead and this period's real-time price "
        "done on a rolling 4 weeks continuously updating prediction "
        "parameters",
    ),
    ForecastMethod(
        alias="gw.me.versant.a1.res.ets",
        category=MarketCategory.Distribution,
        description="Versant Power Residential Electric Thermal Storage "
        "Service Rate Time-of-Use."
        "See https://github.com/thegridelectric/gridworks-ps/tree/dev/docs/enums/distribution_tariff/VersantA1StorageHeatTariff",
    ),
    ForecastMethod(
        alias="isoneexpress.reg.5minfinalrcp.hrlyavg.web",
        category=MarketCategory.Regulation,
        description="Hourly Realtime regulation prices from isoexpress",
    ),
]
