import json
from typing import Optional, Union

from gw.errors import GwTypeError

from gwprice.models import (
    ForecastMethodSql,
    HourlyPriceForecastChannelSql,
    HourlyPriceForecastSql,
    LatestPredictionSql,
    MarketSql,
    PNodeSql,
    PriceSql,
)
from gwprice.type_helpers import ForecastMethod, LatestPrediction, Price

# from gwprice.type_helpers import FinalPrice
from gwprice.types import (
    HourlyPriceForecast,
    HourlyPriceForecastChannel,
    Market,
    PNode
)
from gwprice.types.asl_types import TypeByName
from gwprice.types.gw_base import GwBase


def from_type(msg_bytes: bytes) -> Optional[GwBase]:
    """
    Given an instance of the type (i.e., a serialized byte string for sending
    as a message), returns the appropriate instance of the associated pydantic
    BaseModel class. Returns None if the TypeName is not recogized

    Raises: GwTypeError if msg_bytes fails the type authentication

    Returns: Instance of associated Pydantic object, or None if the
    TypeName is not recognized
    """
    try:
        data = json.loads(msg_bytes.decode("utf-8"))
    except Exception:
        print("failed json loads")
        return None
    return from_dict(data)


def from_dict(data: dict) -> Optional[GwBase]:
    if "TypeName" not in data.keys():
        raise GwTypeError(f"No TypeName - so not a type. Keys: <{data.keys()}>")
    outer_type_name = data["TypeName"]

    # Scada messages all come in a 'gw' incomplete type

    # which has a "Header" and then the payload in a "Payload"
    if outer_type_name == "gw":
        if "Payload" not in data.keys():
            raise GwTypeError(f"Type Gw must include Payload! Keys: <{data.keys()}>")
        data = data["Payload"]
        if "TypeName" not in data.keys():
            raise GwTypeError(f"gw Payload must have TypeName. Keys: {data.keys()}")

    if data["TypeName"] not in TypeByName:
        return None

    return TypeByName[data["TypeName"]].from_dict(data)


def pyd_to_sql(
    t: Union[
        ForecastMethod,
        HourlyPriceForecastChannel,
        HourlyPriceForecast,
        LatestPrediction,
        Market,
        PNode,
        Price,
    ],
) -> Union[
    ForecastMethodSql,
    HourlyPriceForecastChannelSql,
    HourlyPriceForecastSql,
    LatestPredictionSql,
    MarketSql,
    PNodeSql,
    PriceSql,
]:
    d = t.model_dump()
    d.pop("type_name", None)
    d.pop("version", None)

    if isinstance(t, ForecastMethod):
        return ForecastMethodSql(**d)
    elif isinstance(t, HourlyPriceForecastChannel):
        return HourlyPriceForecastChannelSql(**d)
    elif isinstance(t, HourlyPriceForecast):
        return HourlyPriceForecastSql(**d)
    elif isinstance(t, LatestPrediction):
        return LatestPredictionSql(**d)
    elif isinstance(t, Market):
        return MarketSql(**d)
    elif isinstance(t, PNode):
        return PNodeSql(**d)
    elif isinstance(t, Price):
        return PriceSql(**d)
    else:
        raise TypeError(f"Unsupported type: {type(t)}")


def sql_to_pyd(
    t: Union[
        ForecastMethodSql,
        HourlyPriceForecastChannelSql,
        HourlyPriceForecastSql,
        LatestPredictionSql,
        MarketSql,
        PNodeSql,
        PriceSql,
    ],
) -> Union[
    ForecastMethod,
    HourlyPriceForecastChannel,
    HourlyPriceForecast,
    LatestPrediction,
    Market,
    PNode,
    Price,
]:
    d = t.to_dict()
    if isinstance(t, ForecastMethodSql):
        return ForecastMethod(**d)
    elif isinstance(t, HourlyPriceForecastChannelSql):
        return HourlyPriceForecastChannel(**d)
    elif isinstance(t, HourlyPriceForecastSql):
        return HourlyPriceForecast(**d)
    elif isinstance(t, LatestPredictionSql):
        return LatestPrediction(**d)
    elif isinstance(t, MarketSql):
        return Market(**d)
    elif isinstance(t, PNodeSql):
        return PNode(**d)
    elif isinstance(t, PriceSql):
        return Price(**d)
    else:
        raise TypeError(f"Unsupported type: {type(t)}")
