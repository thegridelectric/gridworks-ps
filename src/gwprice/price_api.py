import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pendulum
from pydantic import BaseModel
from gwprice.get_prices_from_isone_api import get_current_lmp, get_hourly_lmp
from gwprice.asl.types.gw0_price_forecast import Gw0PriceForecast
from gwprice.asl.types.gw0_realtime_price import Gw0RealtimePrice


class PriceRequest(BaseModel):
    '''Request for the prices for the visualizer'''
    start_unix_s: float
    end_unix_s: float
    timezone_str: str = 'America/New_York'


class PriceApi():
    def __init__(self):
        self.timezone_str = 'America/New_York'

    def start(self):
        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"], 
            allow_credentials=True,
            allow_methods=["*"],
        )
        self.app.get("/get_forecast_prices/{from_alias}/{type_name}")(self.get_forecast_prices)
        self.app.post("/get_real_time_price/{from_alias}/{type_name}")(self.get_real_time_price)
        self.app.post("/get_prices_visualizer/{from_alias}/{type_name}")(self.get_prices_visualizer)
        uvicorn.run(self.app, host="0.0.0.0", port=8000)

    async def get_prices_visualizer(self, from_alias: str, type_name: str, request: PriceRequest) -> Gw0PriceForecast:
        if from_alias != "hw1-isone-me-versant-keene-ps":
            print(f"Error: from_alias {from_alias} is not supported")
            return
        if type_name != "gw0-price-forecast":
            print(f"Error: type_name {type_name} is not supported")
            return
        start_time = pendulum.from_timestamp(request.start_unix_s, tz=request.timezone_str)
        end_time = pendulum.from_timestamp(request.end_unix_s, tz=request.timezone_str)
        num_days = (end_time.date() - start_time.date()).days
        lmp_prices = []
        for day in range(num_days+1):
            day_time = start_time.add(days=day)
            try:
                prices_day = [
                    x.value for x in get_hourly_lmp(
                        market_name = "e.da60.hw1.isone.4001", 
                        date_str = day_time.strftime("%Y%m%d")
                    )
                ]
            except Exception as e:
                prices_day = []
            if day==0:
                prices_day = prices_day[start_time.hour:]
            if day==num_days:
                prices_day = prices_day[:end_time.hour]
            lmp_prices.extend(prices_day)
        
        all_hours = [start_time.add(hours=i) for i in range(len(lmp_prices))]
        dist_prices = [self.get_dist_price(x.hour, x.weekday()) for x in all_hours]

        result = Gw0PriceForecast(
            from_g_node_alias = from_alias,
            hour_start_s = int(all_hours[0].timestamp()),
            lmp_list = lmp_prices,
            dist_list = dist_prices,
            energy_list = [round(x+y,3) for x,y in zip(lmp_prices, dist_prices)]
        )
        return result

    async def get_forecast_prices(self, from_alias: str, type_name: str) -> Gw0PriceForecast:
        '''Get the forecast prices for the next 48 hours for the specified domain'''
        if from_alias != "hw1-isone-me-versant-keene-ps":
            print(f"Error: from_alias {from_alias} is not supported")
            return
        if type_name != "gw0-price-forecast":
            print(f"Error: type_name {type_name} is not supported")
            return
        try:
            next_hour = pendulum.now(tz=self.timezone_str).add(hours=1).replace(minute=0, second=0, microsecond=0)
            
            # Get the day-ahead prices for today and tomorrow
            try:
                prices_today = [
                    x.value for x in get_hourly_lmp(
                        market_name = "e.da60.hw1.isone.4001", 
                        date_str = next_hour.strftime("%Y%m%d")
                    )
                ]
            except Exception as e:
                raise Exception(f"Error getting today's prices: {e}")
            try:
                prices_tomorrow = [
                    x.value for x in get_hourly_lmp(
                        market_name = "e.da60.hw1.isone.4001", 
                        date_str = next_hour.add(days=1).strftime("%Y%m%d")
                    )
                ]
            except Exception as e:
                prices_tomorrow = []

            # Combine the prices to construct a 48-hour forecast starting from the next hour
            if next_hour.hour <= 12 or not prices_tomorrow:
                lmp_prices = prices_today[next_hour.hour:] + prices_today + prices_today[:next_hour.hour]
            else:
                lmp_prices = prices_today[next_hour.hour:] + prices_tomorrow + prices_tomorrow[:next_hour.hour]

            unix_times = [next_hour.in_timezone(self.timezone_str).timestamp() + i*3600 for i in range(48)]
            dist_prices = [self.get_dist_price(x.hour, x.weekday()) for x in [pendulum.from_timestamp(x) for x in unix_times]]
            energy_prices = [round(x+y, 2) for x, y in zip(lmp_prices, dist_prices)]

            result = Gw0PriceForecast(
                from_g_node_alias = from_alias,
                hour_start_s = int(unix_times[0]),
                lmp_list = lmp_prices,
                dist_list = dist_prices,
                energy_list = energy_prices
            )
            return result

        except Exception as e:
            print(f"Error getting price forecasts: {e}")
            return None

    async def get_real_time_price(self, from_alias: str, type_name: str) -> Gw0RealtimePrice:
        '''Get the real time price for the current 5 minute interval'''
        if from_alias != "hw1-isone-me-versant-keene-ps":
            print(f"Error: from_alias {from_alias} is not supported")
            return
        if type_name != "gw0-realtime-price":
            print(f"Error: type_name {type_name} is not supported")
            return
        now = pendulum.now(tz=self.timezone_str)
        try:
            current_lmp = get_current_lmp(market_name="e.rt60gate5.hw1.isone.ver.keene")
            current_dist = self.get_dist_price(now.hour, now.weekday())
            result = Gw0RealtimePrice(
                from_g_node_alias = from_alias,
                unix_ms = int(now.timestamp()*1000),
                lmp = current_lmp,
                dist = current_dist,
                energy = round(current_lmp + current_dist, 3)
            )
            return result
        except Exception as e:
            print(f"Error getting real time price: {e}")
            return None

    def get_dist_price(self, hour: int, weekday: int):
        return (
            487.63 if hour in [7,8,9,10,11,16,17,18,19] and weekday<5 
            else 54.98 if hour in [12,13,14,15] and weekday<5
            else 50.13
        )

if __name__ == "__main__":
    p = PriceApi()
    p.start()


# ------------------------------------
# BACKUP CODE from aggregator webpage
# ------------------------------------

'''
from pydantic import BaseModel
from typing import List
from pathlib import Path
import csv
import httpx

class PriceUpdate(BaseModel):
    unix_s: List[float]
    lmp: List[float]
    dist: List[float]
'''

'''
self.app.post("/get_default_prices")(self.get_default_prices)
self.app.post("/update_prices")(self.update_prices)
'''

'''
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

async def read_from_csv(self, default=False):
    unix_sec = []
    dist_usd_mwh = []
    lmp_usd_mwh = []
    try:
        if default:
            file_path = Path(f"price_forecast.csv")
        else:
            file_path = Path(f"price_forecast_updated.csv")
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
            print(f"Starting at {pendulum.from_timestamp(unix, tz=self.timezone_str)}")
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
        file_path = Path("price_forecast_updated.csv")
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
'''