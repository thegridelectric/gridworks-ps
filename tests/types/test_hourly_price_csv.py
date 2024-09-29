"""Tests hourly.price.csv type, version 000"""

import pytest
from gw.errors import GwTypeError
from gwprice.types import HourlyPriceCsv


def test_hourly_price_csv_generated() -> None:
    d = {
        "MarketName": "e.rt60gate5.d.isone.ver.keene.stetson",
        "MethodAlias": "gw.pathways.alpha",
        "Comment": "Stetson prices massaged to look like pathways carbon",
        "StartYearUtc": 2020,
        "StartMonthUtc": 1,
        "StartDayUtc": 1,
        "StartHourUtc": 5,
        "StartMinuteUtc": 0,
        "PriceUid": "ed40f2c4-524c-4329-9d9f-fcac2c18d663",
        "Header": "Real Time LMP Electricity Price (Currency Unit/MWh)",
        "PriceList": [124.36, 140.35, 122.42, 122.66],
        "TypeName": "hourly.price.csv",
        "Version": "000",
    }

    assert HourlyPriceCsv.from_dict(d).to_dict() == d

    # TODO: test axiom 1
    d["StartMinuteUtc"] = 20
    with pytest.raises(GwTypeError):
        HourlyPriceCsv.from_dict(d)
