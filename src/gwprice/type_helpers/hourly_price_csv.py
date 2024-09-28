"""Type hourly.price.csv, version 000"""

import csv
from typing import List, Literal

import pendulum
from pydantic import model_validator
from typing_extensions import Self

from gwprice.property_format import LeftRightDot, MarketName, UUID4Str
from gwprice.types.gw_base import GwBase


class HourlyPriceCsv(GwBase):
    market_name: MarketName
    method_alias: LeftRightDot
    comment: str
    start_year_utc: int
    start_month_utc: int
    start_day_utc: int
    start_hour_utc: int
    start_minute_utc: int
    price_uid: UUID4Str
    header: str
    price_list: List[float]
    type_name: Literal["hourly.price.csv"] = "hourly.price.csv"
    version: Literal["000"] = ["000"]

    @model_validator(mode="after")
    def time_check(self) -> Self:
        # Custom validation logic
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

        return self

    def start_unix_s(self) -> int:
        return pendulum.datetime(
            self.start_year_utc,
            self.start_month_utc,
            self.start_day_utc,
            self.start_hour_utc,
            self.start_minute_utc,
        ).int_timestamp

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

        # Process the remaining rows (prices) and add to PriceList
        for row in rows[12:]:
            try:
                price = float(row[0])  # Assuming price data is in the first column
                price_list.append(price)
            except ValueError:
                pass  # Ignore invalid price entries

        d["PriceList"] = price_list
        return cls.from_dict(d)
