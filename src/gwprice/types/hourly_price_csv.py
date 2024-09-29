"""Type hourly.price.csv, version 000"""

import csv
from datetime import datetime, timezone
from typing import List, Literal

import pendulum
from pydantic import StrictInt, model_validator
from typing_extensions import Self

from gwprice.enums import MarketTypeName
from gwprice.property_format import (
    LeftRightDot,
    MarketMinutes,
    MarketName,
    UUID4Str,
)
from gwprice.types.gw_base import GwBase


class HourlyPriceCsv(GwBase):
    market_name: MarketName
    method_alias: LeftRightDot
    comment: str
    start_year_utc: StrictInt
    start_month_utc: StrictInt
    start_day_utc: StrictInt
    start_hour_utc: StrictInt
    start_minute_utc: StrictInt
    price_uid: UUID4Str
    header: str
    price_list: List[float]
    type_name: Literal["hourly.price.csv"] = "hourly.price.csv"
    version: Literal["000"] = "000"

    def market_type(self) -> MarketTypeName:
        x = self.market_name.split(".")
        return x[1]

    def start_unix_s(self) -> int:
        return pendulum.datetime(
            self.start_year_utc,
            self.start_month_utc,
            self.start_day_utc,
            self.start_hour_utc,
            self.start_minute_utc,
        ).int_timestamp

    @model_validator(mode="after")
    def check_axiom_1(self) -> Self:
        """
        Axiom 1: Time Check.
        Validate the start utc points to a valid time. Also, make sure that time is consistent with the market's duration.
        """
        if not (2000 <= self.start_year_utc <= 3000):
            raise ValueError(
                f"StartYearUtc {self.start_year_utc} must be between 2000 and 3000."
            )
        if not (1 <= self.start_month_utc <= 12):
            raise ValueError(
                f"StartMonthUtc {self.start_month_utc} must be between 1 and 12."
            )
        if not (1 <= self.start_day_utc <= 31):
            raise ValueError(
                f"StartDayUtc {self.start_day_utc} must be between 1 and 31."
            )
        if not (0 <= self.start_hour_utc <= 23):
            raise ValueError(
                f"StartHourUtc {self.start_hour_utc} must be between 0 and 23."
            )
        if not (0 <= self.start_minute_utc <= 59):
            raise ValueError(
                f"StartMinuteUtc {self.start_minute_utc} must be between 0 and 59."
            )

        slot_duration_minutes = MarketMinutes[self.market_type()]
        if self.start_unix_s() % (slot_duration_minutes * 60) != 0:
            raise ValueError(
                f"Start {datetime.fromtimestamp(self.start_unix_s(), tz=timezone.utc)} "
                f" not consistent with a market duration {slot_duration_minutes} minutes!"
            )
        return self

    @classmethod
    def from_csv(cls, file_path: str) -> "HourlyPriceCsv":
        d = {}
        price_list = []

        with open(file_path) as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Process the first 12 rows for key-value pairs
        for i, row in enumerate(rows[:12]):
            key, value = row[0].strip(), row[1].strip()
            if key.startswith("\ufeff"):  # Check if it starts with BOM
                key = key[1:]
            d[key] = value
        d["StartYearUtc"] = int(d["StartYearUtc"])
        d["StartMonthUtc"] = int(d["StartMonthUtc"])
        d["StartDayUtc"] = int(d["StartDayUtc"])
        d["StartHourUtc"] = int(d["StartHourUtc"])
        d["StartMinuteUtc"] = int(d["StartMinuteUtc"])
        # Process the remaining rows (prices) and add to PriceList
        for row in rows[12:]:
            try:
                price = float(row[0])  # Assuming price data is in the first column
                price_list.append(price)
            except ValueError:
                pass  # Ignore invalid price entries

        d["PriceList"] = price_list
        return cls.from_dict(d)
