import time
from typing import List, Dict
import pendulum
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4
from contextlib import contextmanager
from gwprice.types import Market
from gwprice.models import HourlyPriceForecastChannelSql as ChannelSql
from gwprice.my_markets import MyMarkets
from gwprice.add_hourly_energy_prices import add_hourly_prices_for_day
import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gwprice.config import Settings
import gwprice.utils as utils
from gwprice.my_hourly_forecast_channels import MyForecastChannels

class PriceServiceHack:
    def __init__(self, settings: Settings, alias: str):
        self.settings = settings
        engine = create_engine(settings.db_url.get_secret_value())
        self.Session = sessionmaker(bind=engine)
        self.world_instance_name = "hw1__1"
        self.alias = alias
        basic_da_channel_names = [ch.name for ch in MyForecastChannels.values() if ch.method_alias == "basic.da" ]
        self.tomorrows_da_exists = {name: False for name in basic_da_channel_names}

    @contextmanager
    def get_session(self):
        """Context manager to provide a new session for each task."""
        session = self.Session()
        try:
            yield session
            session.commit()  # Commit if everything went well
        except Exception:
            session.rollback()  # Rollback in case of an error
            raise  # Re-raise the exception after rollback
        finally:
            session.close()  # Always close the session


    def check_day_ahead_prices_published(self, rt_market: Market) -> bool:
        with self.get_session() as db:
            da_name = utils.rt_to_da_name(rt_market.name)
        ...

"""
WIP. Todo: update day ahead prices as soon as they are available (check
every 10 minutes, sometime between noon and 1 ET every day.)

At 5 minutes after each hour, make and save the next channel forecast 
for all the "basic.da" channels. This means using today's and (if it
is availabe) tomorrow's day ahead prices to estimate the real time price
for the 48 prices starting at the top of next hour. 

Once we make this a rabbit actor, these forecasts will get broadcast
as soon as they are available.

The Atns will get those forecasts and be able to use them when they 
run their FLOs. If the atn misses the forecast it can get it from
the API - but this is meant as a last-minute things. We don't want
to query the API too much right now as we hvae not set up async
access to the database.
"""
