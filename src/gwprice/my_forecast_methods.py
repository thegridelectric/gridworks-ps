from typing import List

from gwprice.types import ForecastMethod

MyForecastMethodDicts = [
    {
        "TypeName": "forecast.method",
        "Version": "000",
        "Alias": "isoneexpress.finalrt.hr.web",
        "Category": "Energy",
        "Description": "Final hourly realtime energy prices from isone isoexpress",
    },
    {
        "TypeName": "forecast.method",
        "Version": "000",
        "Alias": "isoneexpress.da.web",
        "Category": "Energy",
        "Description": "Hourly Day Ahead prices from isoexpress",
    },
    {
        "TypeName": "forecast.method",
        "Version": "000",
        "Alias": "gw.da.predicted.rolling4wks.alpha",
        "Category": "Energy",
        "Description": "Prediction of next period's LMP (electricity price) based on next period's day ahead and this period's real-time price done on a rolling 4 weeks continuously updating prediction parameters",
    },
    {
        "TypeName": "forecast.method",
        "Version": "000",
        "Alias": "gw.me.versant.a1.res.ets",
        "Category": "Distribution",
        "Description": "Versant Power Residential Electric Thermal Storage Service Rate Time-of-Use.See https://github.com/thegridelectric/gridworks-ps/tree/dev/docs/enums/distribution_tariff/VersantA1StorageHeatTariff",
    },
    {
        "TypeName": "forecast.method",
        "Version": "000",
        "Alias": "isoneexpress.reg.5minfinalrcp.hrlyavg.web",
        "Category": "Regulation",
        "Description": "Hourly Realtime regulation prices from isoexpress",
    },
    {
        "TypeName": "forecast.method",
        "Version": "000",
        "Alias": "gw.pathways.alpha",
        "Category": "Energy",
        "Description": "Stetson prices massaged to look like pathways carbon, done by George.",
    },
    {
        "TypeName": "forecast.method",
        "Version": "000",
        "Alias": "gw.pathways.beta",
        "Category": "Energy",
        "Description": "Prediction of next period's LMP (electricity price) based on next period's day ahead and this period's real-time price done on a rolling 4 weeks continuously updating prediction parameters",
    },
    {
        "TypeName": "forecast.method",
        "Version": "000",
        "Alias": "basic.da",
        "Category": "Energy",
        "Description": "Use DA prices for today, and once tomorrows prices are available (typically between noon and 1 America/NY) use those prices for  tomorrow.  In either case, repeat the last day for the remaining  hours",
    },
]

MyForecastMethods: List[ForecastMethod] = [
    ForecastMethod.from_dict(d) for d in MyForecastMethodDicts
]
