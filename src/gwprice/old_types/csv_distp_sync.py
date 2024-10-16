import csv
import datetime
from typing import Any, Dict, List, NamedTuple, Optional, Tuple

import numpy as np
from gridworks import property_format
from gridworks.errors import SchemaError


class CsvDistpSync(NamedTuple):
    PNodeAlias: str
    MethodAlias: str
    Comment: str
    StartYearUtc: int
    StartMonthUtc: int
    StartDayUtc: int
    StartHourUtc: int
    StartMinuteUtc: int
    UniformSliceDurationHrs: float
    TimezoneString: str
    CurrencyUnit: str
    PriceUid: str
    Header: str
    Prices: list
    TypeName: str = "csv.distp.sync"

    def asdict(self):
        d = self._asdict()
        return d

    def is_valid(self) -> Tuple[bool, Optional[List[str]]]:
        is_valid, errors = self.passes_derived_validations()
        return is_valid, errors

    def passes_derived_validations(self) -> Tuple[bool, Optional[List[str]]]:
        is_valid = True
        errors = []
        if self.TypeName != "csv.distp.sync":
            is_valid = False
            errors.append(
                f"Payload requires TypeName of 'csv.distp.sync', not {self.TypeName}."
            )
        if not isinstance(self.PNodeAlias, str):
            is_valid = False
            errors.append("PNodeAlias must have type str.")
        if not isinstance(self.StartYearUtc, int):
            is_valid = False
            errors.append("StartYearUtc must have type int.")
        if not isinstance(self.StartMonthUtc, int):
            is_valid = False
            errors.append("StartMonthUtc must have type int.")
        if not isinstance(self.StartDayUtc, int):
            is_valid = False
            errors.append("StartDayUtc must have type int.")
        if not isinstance(self.StartHourUtc, int):
            is_valid = False
            errors.append("StartHourUtc must have type int.")
        if not isinstance(self.StartMinuteUtc, int):
            is_valid = False
            errors.append("StartMinuteUtc must have type int.")
        try:
            datetime.datetime(
                year=self.StartYearUtc,
                month=self.StartMonthUtc,
                day=self.StartDayUtc,
                hour=self.StartHourUtc,
                minute=self.StartMinuteUtc,
            )
        except ValueError as e:
            is_valid = False
            errors.append(e)
        if not isinstance(self.UniformSliceDurationHrs, float):
            is_valid = False
            errors.append("UniformSliceDurationHrs must have type float.")
        if not isinstance(self.CurrencyUnit, str):
            is_valid = False
            errors.append(f"CurrencyUnit {self.CurrencyUnit} must have type str.")
        if not isinstance(self.PriceUid, str):
            is_valid = False
            errors.append(f"PriceUid {self.PriceUid} must have type str.")
        if not property_format.is_uuid_canonical_textual(self.PriceUid):
            is_valid = False
            errors.append(
                f"PriceUid {self.PriceUid} must have format UuidCanonicalTextual."
            )

        return is_valid, errors


class CsvDistpSync_Maker:
    type_name = "csv.distp.sync"

    @classmethod
    def payload_is_valid(
        cls, payload_as_dict: Dict[str, Any]
    ) -> Tuple[bool, Optional[List[str]]]:
        try:
            payload_as_dict["UniformSliceDurationHrs"] = float(
                payload_as_dict["UniformSliceDurationHrs"]
            )
        except ValueError:
            pass  # This will get caught in is_valid() check below
        try:
            p = CsvDistpSync(
                TypeName=payload_as_dict["TypeName"],
                PNodeAlias=payload_as_dict["PNodeAlias"],
                MethodAlias=payload_as_dict["MethodAlias"],
                Comment=payload_as_dict["Comment"],
                StartYearUtc=payload_as_dict["StartYearUtc"],
                StartMonthUtc=payload_as_dict["StartMonthUtc"],
                StartDayUtc=payload_as_dict["StartDayUtc"],
                StartHourUtc=payload_as_dict["StartHourUtc"],
                StartMinuteUtc=payload_as_dict["StartMinuteUtc"],
                TimezoneString=payload_as_dict["TimezoneString"],
                CurrencyUnit=payload_as_dict["CurrencyUnit"],
                PriceUid=payload_as_dict["PriceUid"],
                Header=payload_as_dict["Header"],
                UniformSliceDurationHrs=payload_as_dict["UniformSliceDurationHrs"],
                Prices=payload_as_dict["Prices"],
            )
        except TypeError:
            errors = [TypeError]
            return False, errors
        return p.is_valid()

    def __init__(self, dist_price_file):
        self.errors = []
        self.tuple: Optional[CsvDistpSync] = None
        first_data_row = 14
        prices = np.array([])

        with open(dist_price_file, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            line_idx = 0
            for row in reader:
                if line_idx == 0:
                    property = row[0].replace("\ufeff", "")
                    type_name = row[1]
                    if property != "TypeName":
                        raise Exception(
                            f"Csv 0,0 must be TypeName, instead it is {property}"
                        )
                if line_idx == 1:
                    property = row[0]
                    p_node_alias = row[1].strip()
                    if property != "PNodeAlias":
                        raise Exception(
                            f"Csv 1,0 must be PNodeAlias, instead it is {property}"
                        )
                if line_idx == 2:
                    property = row[0]
                    method_alias = row[1].strip()
                    if property != "MethodAlias":
                        raise Exception(
                            f"Csv 2,0 must be MethodAlias, instead it is {property}"
                        )
                if line_idx == 3:
                    property = row[0]
                    comment = row[1].strip()
                    if property != "Comment":
                        raise Exception(
                            f"Csv 3,0 must be Comment, instead it is {property}"
                        )
                if line_idx == 4:
                    property = row[0]
                    start_year_utc = int(row[1])
                    if property != "StartYearUtc":
                        raise Exception(
                            f"Csv 4,0 must be StartYearUtc, instead it is {property}"
                        )
                if line_idx == 5:
                    property = row[0]
                    start_month_utc = int(row[1])
                    if property != "StartMonthUtc":
                        raise Exception(
                            f"Csv 5,0 must be StartMonthUtc, instead it is {property}"
                        )
                if line_idx == 6:
                    property = row[0]
                    start_day_utc = int(row[1])
                    if property != "StartDayUtc":
                        raise Exception(
                            f"Csv 6,0 must be StartDayUtc, instead it is {property}"
                        )
                if line_idx == 7:
                    property = row[0]
                    start_hour_utc = int(row[1])
                    if property != "StartHourUtc":
                        raise Exception(
                            f"Csv 7,0 must be StartHourUtc, instead it is {property}"
                        )
                if line_idx == 8:
                    property = row[0]
                    start_minute_utc = int(row[1])
                    if property != "StartMinuteUtc":
                        raise Exception(
                            f"Csv 8,0 must be StartMinuteUtc, instead it is {property}"
                        )
                if line_idx == 9:
                    property = row[0]
                    uniform_slice_duration_hrs = float(row[1])
                    if property != "UniformSliceDurationHrs":
                        raise Exception(
                            f"Csv 9,0 must be UniformSliceDurationHrs, instead it is {property}"
                        )
                if line_idx == 10:
                    property = row[0]
                    timezone_string = row[1]
                    if property != "TimezoneString":
                        raise Exception(
                            f"Csv 10,0 must be TimezoneString, instead it is {property}"
                        )
                if line_idx == 11:
                    property = row[0]
                    currency_unit = row[1].strip()
                    if property != "CurrencyUnit":
                        raise Exception(
                            f"Csv 11,0 must be CurrencyUnit, instead it is {property}"
                        )
                if line_idx == 12:
                    property = row[0]
                    price_uid = row[1].strip()
                    if property != "PriceUid":
                        raise Exception(
                            f"Csv 12,0 must be PriceUid, instead it is {property}"
                        )
                if line_idx == 13:
                    property = row[0]
                    header = row[1].strip()
                    if property != "Header":
                        raise Exception(
                            f"Csv 13,0 must be Header, instead it is {property}"
                        )
                    if header != "Distribution Electricity Price (Currency Unit/MWh)":
                        raise Exception(
                            f"Csv 13,1 must be 'Distribution Electricity Price (Currency Unit/MWh)', instead it is '{header}'"
                        )
                elif line_idx >= first_data_row:
                    try:
                        prices = np.append(prices, float(row[0]))
                    except ValueError:
                        raise Exception(f"Missing a price in row {line_idx + 1}")
                line_idx += 1

        p = CsvDistpSync(
            TypeName=type_name,
            PNodeAlias=p_node_alias,
            MethodAlias=method_alias,
            Comment=comment,
            StartYearUtc=start_year_utc,
            StartMonthUtc=start_month_utc,
            StartDayUtc=start_day_utc,
            StartHourUtc=start_hour_utc,
            StartMinuteUtc=start_minute_utc,
            UniformSliceDurationHrs=uniform_slice_duration_hrs,
            TimezoneString=timezone_string,
            CurrencyUnit=currency_unit,
            PriceUid=price_uid,
            Header=header,
            Prices=list(prices),
        )

        is_valid, errors = p.is_valid()
        if is_valid is False:
            self.errors = errors
            print(errors)
            raise SchemaError(
                f"Failed to create payload due to these errors:{errors}. Input file is {dist_price_file}"
            )
        else:
            self.tuple = p
