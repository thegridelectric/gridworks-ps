import time
import uuid
import dotenv
import uvicorn
import zipfile
import pendulum
import traceback
import numpy as np
import pandas as pd
from datetime import timedelta
from pydantic import BaseModel, Field
from typing import List, Optional, Union
import asyncio
import async_timeout
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from pathlib import Path
import csv
import pytz
from datetime import datetime

class PriceUpdate(BaseModel):
    newLmpList: List[float]
    newTariffList: List[float]


class PriceApi():
    def __init__(self, running_locally):
        self.running_locally = running_locally        
        self.timezone_str = 'America/New_York'
        self.timezone = pytz.timezone(self.timezone_str)
        self.timeout_seconds = 3*60

    def start(self):
        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            # TODO: allow_origins=["https://thegridelectric.github.io"]
            allow_origins=["*"], 
            allow_credentials=True,
            allow_methods=["*"],
        )
        self.app.post("/get_prices")(self.get_prices)
        self.app.post("/get_default_prices")(self.get_default_prices)
        self.app.post("/update_prices")(self.update_prices)
        uvicorn.run(self.app, host="0.0.0.0", port=8000)

    async def get_default_prices(self):
        prices = await self.read_from_csv(default=True)
        return prices

    async def get_prices(self):
        prices = await self.read_from_csv(default=False)
        return prices

    async def read_from_csv(self, default=False):
        dist_usd_mwh = []
        lmp_usd_mwh = []
        try:
            if default:
                file_path = Path(f"basic_api/price_forecast.csv")
            else:
                file_path = Path(f"basic_api/price_forecast_updated.csv")
            with open(file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    dist_usd_mwh.append(float(row[0]))
                    lmp_usd_mwh.append(float(row[1]))
                if len(dist_usd_mwh)<72 or len(lmp_usd_mwh)<72:
                    raise Exception("Price forecasts must be at least 72 hours long")
        except Exception as e:
            raise Exception(e)
        
        if datetime.now(tz=self.timezone) < datetime(2025, 2, 20, 17, tzinfo=self.timezone):
            # Get the current hour
            now = datetime.now(tz=self.timezone)
            current_hour = now.hour
            day_offset = (now.day % 3) * 24
            # Calculate the starting hour for the 48-hour forecast
            start_hour = (day_offset + current_hour + 1) % 72
            # Wrap the lists for the 48-hour forecast
            dp_forecast_usd_per_mwh = [dist_usd_mwh[(start_hour + i) % 72] for i in range(48)]
            lmp_forecast_usd_per_mwh = [lmp_usd_mwh[(start_hour + i) % 72] for i in range(48)]
        else:
            time_since_21_feb = (datetime.now(tz=self.timezone).replace(minute=0, second=0, microsecond=0)
                                 - datetime(2025, 2, 20, 17, tzinfo=self.timezone))
            start_hour = int(time_since_21_feb.total_seconds() / 3600)
            dp_forecast_usd_per_mwh = [dist_usd_mwh[start_hour + i] for i in range(48)]
            lmp_forecast_usd_per_mwh = [lmp_usd_mwh[start_hour + i] for i in range(48)]

        result = {
            'lmp': lmp_forecast_usd_per_mwh,
            'dist': dp_forecast_usd_per_mwh,
            'energy': [round(x+y,2) for x,y in zip(dp_forecast_usd_per_mwh, lmp_forecast_usd_per_mwh)]
        }
        return result
    
    async def update_prices(self, prices: PriceUpdate):
        try:
            time_since_21_feb = (datetime.now(tz=self.timezone).replace(minute=0, second=0, microsecond=0)
                                - datetime(2025, 2, 20, 17, tzinfo=self.timezone))
            start_hour = int(time_since_21_feb.total_seconds() / 3600)

            file_path = Path(f"basic_api/price_forecast_updated.csv")

            rows = []
            with open(file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    rows.append(row)

            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Tariff", "LMP"])
                idx = 0
                for row in rows:
                    if start_hour <= idx < start_hour + 24:
                        new_tariff = prices.newTariffList[idx - start_hour]
                        new_lmp = prices.newLmpList[idx - start_hour]
                        writer.writerow([new_tariff, new_lmp])
                    else:
                        writer.writerow([float(row[0]), float(row[1])])
                    idx += 1

            prices = await self.read_from_csv(default=False)
            return prices

        except Exception as e:
            print(f"An error occurred while updating the prices: {str(e)}")
            raise Exception("Failed to update prices")



p = PriceApi(running_locally=True)
p.start()