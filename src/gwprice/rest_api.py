from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from gwprice.codec import sql_to_pyd
from gwprice.database import get_db
from gwprice.models import (
    HourlyPriceForecastChannelSql,
    HourlyPriceForecastSql,
    PNodeSql,
)
from gwprice.types import HourlyPriceForecast, HourlyPriceForecastChannel, PNode

# Initialize
app = FastAPI()


@app.get("/p_nodes", response_model=List[PNode])
def get_p_nodes(db: Session = Depends(get_db)) -> List[PNode]:
    sql_p_nodes = db.query(PNodeSql).all()
    p_nodes = [sql_to_pyd(p_node) for p_node in sql_p_nodes]
    return p_nodes


@app.get("/channels", response_model=List[HourlyPriceForecastChannel])
def get_channels(db: Session = Depends(get_db)) -> List[HourlyPriceForecastChannelSql]:
    sql_channels = db.query(HourlyPriceForecastChannelSql).all()
    channels = [sql_to_pyd(channel) for channel in sql_channels]
    return channels


@app.get(
    "/forecast/{channel_name}/{start_unix_s}",
    response_model=Optional[HourlyPriceForecast],
)
def get_latest_forecast(
    channel_name: str, start_unix_s: int, db: Session = Depends(get_db)
) -> Optional[HourlyPriceForecast]:
    # Query for the latest forecast matching the given channel_name and start_unix_s
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
