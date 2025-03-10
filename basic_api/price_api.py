import uvicorn
from pydantic import BaseModel, Field
from typing import List, Optional, Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import csv
import pytz
from datetime import datetime
import httpx
import time
import os
import pendulum

class PriceUpdate(BaseModel):
    unix_s: List[float]
    lmp: List[float]
    dist: List[float]


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

    async def send_to_visualizer_api(self, data):
        url = "https://visualizer.electricity.works/prices"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data)
                if response.status_code == 200:
                    print("Successfully sent prices to visualizer API")
                    return response.json()
                else:
                    print(f"Failed to send data. Status code: {response.status_code}")
                    return None
        except httpx.RequestError as e:
            print(f"An error occurred while sending data: {e}")
            return None

    async def get_default_prices(self):
        prices = await self.read_from_csv(default=True)
        return prices

    async def get_prices(self):
        prices = await self.read_from_csv(default=False)
        return prices

    async def read_from_csv(self, default=False):
        unix_sec = []
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
                    try:
                        unix_sec.append(float(row[0]))
                        dist_usd_mwh.append(float(row[1]))
                        lmp_usd_mwh.append(float(row[2]))
                    except:
                        continue
        except Exception as e:
            raise Exception(e)
        
        current_time = time.time()
        start_index = None
        for i, unix in enumerate(unix_sec):
            if unix > current_time:
                print(f"Starting at {pendulum.from_timestamp(unix, tz='America/New_York')}")
                start_index = i
                break
        end_index = start_index + 48
        
        result = {
            'unix_s': unix_sec[start_index:end_index],
            'lmp': lmp_usd_mwh[start_index:end_index],
            'dist': dist_usd_mwh[start_index:end_index],
            'energy': [round(x + y, 2) for x, y in zip(lmp_usd_mwh[start_index:end_index], 
                                                       dist_usd_mwh[start_index:end_index])]
        }
        return result
    
    async def update_prices(self, prices: PriceUpdate):
        try:
            rows = []
            file_path = Path("basic_api/price_forecast_updated.csv")
            with open(file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader)
                rows = list(reader)

            updated_prices = {float(timestamp): (lmp, dist) 
                            for timestamp, lmp, dist in zip(prices.unix_s, prices.lmp, prices.dist)}

            # Update the rows based on the new prices
            for row in rows:
                try:
                    unix_timestamp = float(row[0])
                    if unix_timestamp in updated_prices:
                        lmp, dist = updated_prices[unix_timestamp]
                        row[1] = dist
                        row[2] = lmp
                except Exception as e:
                    print(f"Error processing row {row}: {e}")
                    continue

            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(rows)

            print(f"Prices updated successfully in {file_path}")

            final_prices = await self.read_from_csv()
            await self.send_to_visualizer_api(final_prices)
            return final_prices

        except Exception as e:
            print(f"Error updating prices: {e}")


p = PriceApi(running_locally=True)
p.start()