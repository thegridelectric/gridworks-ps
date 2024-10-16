import time
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import and_, desc
from sqlalchemy.orm import Session

from gwprice.codec import sql_to_pyd
from gwprice.database import get_db
from gwprice.models import (
    ForecastMethodSql,
    HourlyPriceForecastChannelSql,
    HourlyPriceForecastSql,
    PNodeSql,
)
from gwprice.types import (
    ForecastMethod,
    HourlyPriceForecast,
    HourlyPriceForecastChannel,
    PNode,
)

# Initialize
app = FastAPI()


@app.get("/hello")
def get_hello():
    return {"hi": "there"}

@app.get("/p-nodes", response_model=List[PNode])
def get_p_nodes(db: Session = Depends(get_db)) -> List[PNode]:
    sql_p_nodes = db.query(PNodeSql).all()
    p_nodes = [sql_to_pyd(p_node) for p_node in sql_p_nodes]
    return p_nodes


@app.get("/channels", response_model=List[HourlyPriceForecastChannel])
def get_channels(db: Session = Depends(get_db)) -> List[HourlyPriceForecastChannel]:
    sql_channels = db.query(HourlyPriceForecastChannelSql).all()
    channels = [sql_to_pyd(channel) for channel in sql_channels]
    return channels


@app.get("/forecast-methods", response_model=List[ForecastMethod])
def get_forecast_methods(db: Session = Depends(get_db)) -> List[ForecastMethod]:
    sql_methods = db.query(ForecastMethodSql).all()
    methods = [sql_to_pyd(method) for method in sql_methods]
    return methods


@app.get(
    "/forecast/{channel_name_lrh}/{start_unix_s}",
    response_model=Optional[HourlyPriceForecast],
)
def get_forecast(
    channel_name_lrh: str, start_unix_s: int, db: Session = Depends(get_db)
) -> Optional[HourlyPriceForecast]:
    # Query for the latest forecast matching the given channel_name and start_unix_s
    channel_name = channel_name_lrh.replace("-", ".")
    forecast = (
        db.query(HourlyPriceForecastSql)
        .filter(HourlyPriceForecastSql.channel_name == channel_name)
        .filter(HourlyPriceForecastSql.start_unix_s == start_unix_s)
        .order_by(
            desc(HourlyPriceForecastSql.forecast_created_s)
        )  # Get the latest created forecast
        .first()
    )

    if forecast is None:
        raise HTTPException(status_code=404, detail="Forecast not found")

    # Return the forecast as a Pydantic model
    return forecast


@app.get(
    "/forecast_by_id/{price_uid}",
    response_model=Optional[HourlyPriceForecast],
)
def get_forecast_by_id(
    price_uid: str, db: Session = Depends(get_db)
) -> Optional[HourlyPriceForecast]:
    forecast = (
        db.query(HourlyPriceForecastSql)
        .filter(HourlyPriceForecastSql.price_uid == price_uid)
        .first()
    )
    if forecast is None:
        raise HTTPException(status_code=404, detail="Forecast not found")

    # Return the forecast as a Pydantic model
    return forecast


@app.get(
    "/latest-forecast/{channel_name_lrh}",
    response_model=Optional[HourlyPriceForecast],
)
def get_latest_forecast(
    channel_name_lrh: str, db: Session = Depends(get_db)
) -> Optional[HourlyPriceForecast]:
    channel_name = channel_name_lrh.replace("-", ".")
    current_time = int(time.time())

    # Query to find forecasts with the specified channel name and conditions
    forecast = (
        db.query(HourlyPriceForecastSql)
        .filter(
            and_(
                HourlyPriceForecastSql.channel_name == channel_name,
                HourlyPriceForecastSql.start_unix_s > current_time,
                HourlyPriceForecastSql.forecast_created_s.isnot(None),
            )
        )
        .order_by(HourlyPriceForecastSql.forecast_created_s.desc())
        .first()  # Get the first result with the largest forecast_created_s
    )
    if forecast is None:
        raise HTTPException(status_code=404, detail="Forecast not found")

    # Return the forecast as a Pydantic model
    return forecast
