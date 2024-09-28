from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from gwprice.types import PNode
from gwprice.database import get_db
from gwprice.models import PNodeSql
from gwprice.models import HourlyPriceForecastChannelSql
from gwprice.types import HourlyPriceForecastChannel
from gwprice.codec import sql_to_pyd

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