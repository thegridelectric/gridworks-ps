"""JournalKeeper"""

import logging
import threading
import time
from contextlib import contextmanager

import pendulum
from gw.named_types import GwBase
from gwbase.actor_base import ActorBase
from gwbase.codec import GwCodec
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gwprice.codec import pyd_to_sql, sql_to_pyd
from gwprice.config import Settings
from gwprice.models import (
    HourlyPriceForecastSql,
    PriceSql,
    bulk_insert_prices
)

from gwprice.named_types.asl_types import TypeByName
from gwprice.type_helpers import Price
from gwprice.named_types import HourlyPriceForecast

LOG_FORMAT = (
    "%(levelname) -10s %(sasctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)


class PriceService(ActorBase):
    def __init__(self, settings: Settings):
        # use our knwon types
        super().__init__(settings=settings, codec=GwCodec(type_by_name=TypeByName))
        self.settings: Settings = settings
        self._consume_exchange = "ear_tx"
        engine = create_engine(settings.db_url.get_secret_value())
        self.Session = sessionmaker(bind=engine)
        self.main_thread = threading.Thread(target=self.main)


    def local_start(self) -> None:
        """This overwrites local_start in actor_base, used for additional threads.
        It cannot assume the rabbit channels are established and that
        messages can be received or sent."""
        self.main_thread.start()
        self._main_loop_running = True
        print("Just started main thread")

    def local_stop(self) -> None:
        self._main_loop_running = False
        self.main_thread.join()

    @contextmanager
    def get_db(self):
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

    ########################
    ## Receives
    ########################

    def route_message(self, from_alias: str, payload: GwBase) -> None:
        t = time.time()
        ft = pendulum.from_timestamp(t, tz="America/New_York").format(
            "YYYY-MM-DD HH:mm:ss.SSS"
        )
        short_alias = from_alias.split(".")[-2]
        print(f"[{ft}] {payload.type_name} from {short_alias}")
        print("Does not process any messages yet!")

    def main(self) -> None:
        while True:
            time.sleep(3600)
            
