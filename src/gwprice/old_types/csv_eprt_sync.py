import csv
import datetime
import uuid
from typing import Any
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Tuple

import numpy as np
import pendulum
from gridworks.errors import DcError
from gridworks.errors import SchemaError

import gwatn.types.hack_property_format as property_format
from gwatn.types.hack_test_dummy import TEST_DUMMY_AGENT
from gwatn.types.hack_utils import camel_to_snake
from gwatn.types.hack_utils import log_style_utc_date_w_millis
from gwatn.types.hack_utils import snake_to_camel
from gwatn.types.ps_electricityprices_gnode.r_eprt_sync.r_eprt_sync_1_0_0 import (
    Payload as REprtSync100Payload,
)
from gwatn.types.ps_electricityprices_gnode.r_eprt_sync.r_eprt_sync_1_0_0 import (
    R_Eprt_Sync_1_0_0,
)


class Payload(NamedTuple):
    MpAlias: str
    WorldInstanceAlias: str
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
    MessageId: str

    def asdict(self):
        d = self._asdict()
        return d

    def is_valid(self) -> Tuple[bool, Optional[List[str]]]:
        is_valid, errors = self.passes_derived_validations()
        return is_valid, errors

    def passes_derived_validations(self) -> Tuple[bool, Optional[List[str]]]:
        is_valid = True
        errors = []
        if self.MpAlias != "csv.eprt.sync.1_0_0":
            is_valid = False
            errors.append(
                f"Payload requires MpAlias of 'csv.eprt.sync.1_0_0', not {self.MpAlias}."
            )
        if not isinstance(self.WorldInstanceAlias, str):
            is_valid = False
            errors.append(
                f"WorldInstanceAlias {self.WorldInstanceAlias} must have type str."
            )
        if not property_format.is_world_instance_alias_format(self.WorldInstanceAlias):
            is_valid = False
            errors.append(
                f"WorldInstanceAlias {self.WorldInstanceAlias} must have format WorldInstanceAliasFormat"
            )
        if not isinstance(self.PNodeAlias, str):
            is_valid = False
            errors.append(f"PNodeAlias must have type str.")
        if not property_format.is_recognized_p_node_alias(self.PNodeAlias):
            is_valid = False
            errors.append(
                f"PNodeAlias {self.PNodeAlias} must have format RecognizedPNodeAlias."
            )
        if not isinstance(self.StartYearUtc, int):
            is_valid = False
            errors.append(f"StartYearUtc must have type int.")
        if not isinstance(self.StartMonthUtc, int):
            is_valid = False
            errors.append(f"StartMonthUtc must have type int.")
        if not isinstance(self.StartDayUtc, int):
            is_valid = False
            errors.append(f"StartDayUtc must have type int.")
        if not isinstance(self.StartHourUtc, int):
            is_valid = False
            errors.append(f"StartHourUtc must have type int.")
        if not isinstance(self.StartMinuteUtc, int):
            is_valid = False
            errors.append(f"StartMinuteUtc must have type int.")
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
            errors.append(f"UniformSliceDurationHrs must have type float.")
        if not isinstance(self.TimezoneString, str):
            is_valid = False
            errors.append(f"TimezoneString {self.TimezoneString} must have type str.")
        if not isinstance(self.CurrencyUnit, str):
            is_valid = False
            errors.append(f"CurrencyUnit {self.CurrencyUnit} must have type str.")
        if not property_format.is_recognized_currency_unit(self.CurrencyUnit):
            is_valid = False
            errors.append(
                f"CurrencyUnit {self.CurrencyUnit} must have format RecognizedCurrencyUnit."
            )
        if not isinstance(self.PriceUid, str):
            is_valid = False
            errors.append(f"PriceUid {self.PriceUid} must have type str.")
        if not property_format.is_uuid_canonical_textual(self.PriceUid):
            is_valid = False
            errors.append(
                f"PriceUid {self.PriceUid} must have format UuidCanonicalTextual."
            )
        if not isinstance(self.MessageId, str):
            is_valid = False
            errors.append(f"MessageId {self.MessageId} must have type str.")
        if not property_format.is_uuid_canonical_textual(self.MessageId):
            is_valid = False
            errors.append(
                f"MessageId {self.MessageId} must have format UuidCanonicalTextual."
            )
        # TODO: add rest of validations

        return is_valid, errors


class Csv_Eprt_Sync_1_0_0:
    mp_alias = "csv.eprt.sync.1_0_0"

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
            p = Payload(
                MpAlias=payload_as_dict["MpAlias"],
                WorldInstanceAlias=payload_as_dict["WorldInstanceAlias"],
                PNodeAlias=payload_as_dict["PNodeAlias"],
                MethodAlias=payload_as_dict["MethodAlias"],
                Comment=payload_as_dict["Comment"],
                StartYearUtc=payload_as_dict["StartYearUtc"],
                StartMonthUtc=payload_as_dict["StartMonthUtc"],
                StartDayUtc=payload_as_dict["StartDayUtc"],
                StartHourUtc=payload_as_dict["StartHourUtc"],
                StartMinuteUtc=payload_as_dict["StartMinuteUtc"],
                UniformSliceDurationHrs=payload_as_dict["UniformSliceDurationHrs"],
                TimezoneString=payload_as_dict["TimezoneString"],
                CurrencyUnit=payload_as_dict["CurrencyUnit"],
                PriceUid=payload_as_dict["PriceUid"],
                Header=payload_as_dict["Header"],
                Prices=payload_as_dict["Prices"],
                MessageId=payload_as_dict["MessageId"],
            )
        except TypeError:
            errors = [TypeError]
            return False, errors
        return p.is_valid()

    def __init__(self, real_time_electricity_price_csv):
        file = real_time_electricity_price_csv
        self.errors = []
        self.payload = None
        first_data_row = 14
        prices = np.array([])
        uniform_slice_duration_hrs = np.array([])
        with open(real_time_electricity_price_csv, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            line_idx = 0
            for row in reader:
                if line_idx == 0:
                    property = row[0].replace("\ufeff", "")
                    mp_alias = row[1]
                    if property != "MpAlias":
                        raise Exception(
                            f"Csv 0,0 must be MpAlias, instead it is {property}"
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
                            f"Csv 2,0 must be MethodAlias, instead it is {property}. Check file {file}."
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
                    timezone_string = row[1].strip()
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
                    if header != "Real Time LMP Electricity Price (Currency Unit/MWh)":
                        raise Exception(
                            f"Csv 13,1 must be 'Real Time LMP Electricity Price (Currency Unit/MWh)', instead it is {header}"
                        )
                elif line_idx >= first_data_row:
                    try:
                        prices = np.append(prices, float(row[0]))
                    except ValueError:
                        raise Exception(f"Missing a price in row {line_idx+1}")
                line_idx += 1

        p = Payload(
            MpAlias=mp_alias,
            WorldInstanceAlias="dw1__1",
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
            MessageId=str(uuid.uuid4()),
        )

        is_valid, errors = p.is_valid()
        if is_valid is False:
            self.errors = errors
            print(errors)
            raise SchemaError(
                f"Failed to create payload due to these errors:{errors}. Input file is {real_time_electricity_price_csv}"
            )
        else:
            self.payload = p

    def paired_rabbit_payload(self, agent=TEST_DUMMY_AGENT) -> REprtSync100Payload:
        start_utc = pendulum.datetime(
            year=self.payload.StartYearUtc,
            month=self.payload.StartMonthUtc,
            day=self.payload.StartDayUtc,
            hour=self.payload.StartHourUtc,
            minute=self.payload.StartMinuteUtc,
        )

        return R_Eprt_Sync_1_0_0(
            agent=agent,
            prices=self.payload.Prices,
            uniform_slice_duration_hrs=self.payload.UniformSliceDurationHrs,
            method_alias=self.payload.MethodAlias,
            start_utc=start_utc,
            currency_unit=self.payload.CurrencyUnit,
            p_node_alias=self.payload.PNodeAlias,
            price_uid=self.payload.PriceUid,
            timezone_string=self.payload.TimezoneString,
            comment=self.payload.Comment,
        ).payload


