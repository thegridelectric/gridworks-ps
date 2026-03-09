import requests
import httpx
import csv
import time
import json
from pathlib import Path
from typing import List
from datetime import datetime
import pytz
from gwprice.asl.types.gw0_price_forecast import Gw0PriceForecast
from gwprice.asl.types.gw0_realtime_price import Gw0RealtimePrice

running_locally = True

if running_locally:
    HOST = "http://0.0.0.0:8000"
else:
    HOST = "https://price-service.electricity.works"


# Additional
from pydantic import BaseModel

class PriceForecast(BaseModel):
    dp_usd_per_mwh: List[float]
    lmp_usd_per_mwh: List[float]
    reg_usd_per_mwh: List[float]

    @property
    def total_energy(self) -> List[float]:
        """Calculate the total price forecast by summing dp, lmp, and reg components."""
        return [dp + lmp for dp, lmp in zip(self.dp_usd_per_mwh, self.lmp_usd_per_mwh)]
        

async def get_real_time_price() -> float:
    '''Returns current 5min real-time price (LMP+Dist) in USD/MWh'''
    try:
        url = f"{HOST}/hw1-isone-me-versant-keene-ps/gw0-realtime-price"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                print("Successfully received prices from API")
                data = response.json()
                price = Gw0RealtimePrice(**data)
                return price.energy
            else:
                print(f"Failed to receive prices from API, status code: {response.status_code}")
                raise Exception("Failed to receive prices.")
    except Exception as e:
        print(f"Error getting current price: {e}")
        try:
            print("Attempt to use the forecast price instead of current price")
            price = await read_forecasted_price_for_now()
            return price
        except Exception as e:
            print(f"Error getting forecast price: {e}")
            return 0

async def get_price_forecast_48h(data_dir: str = "./data") -> PriceForecast:
    '''Gets price forecast for the next 48 hours. All in USD/MWh'''
    try:
        # Get price forecast from the price service API
        url = f"{HOST}/hw1-isone-me-versant-keene-ps/gw0-price-forecast"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                print("Successfully received price forecast from the price service API")
                data = response.json()
                price_forecast = Gw0PriceForecast(**data)
                print(f"- LMP USD/MWh {price_forecast.lmp_list}")
                print(f"- Total energy USD/MWh {[round(x,2) for x in price_forecast.energy_list]}")
                
                # Save price forecast to a local CSV file
                Path(data_dir).mkdir(exist_ok=True)
                prices_file = Path(f"{data_dir}/price_forecast.csv")
                
                # Check if current hour's data exists in the existing file
                current_hour_row = None
                if prices_file.exists():
                    current_hour_timestamp = price_forecast.hour_start_s[0] - 3600
                    with open(prices_file, 'r', newline='') as f:
                        reader = csv.reader(f)
                        header = next(reader)
                        for row in reader:
                            if float(row[0]) == current_hour_timestamp:
                                current_hour_row = row
                                print(f"DEBUG: Found current hour data: {current_hour_timestamp} == {datetime.fromtimestamp(current_hour_timestamp, tz=pytz.timezone('America/New_York'))}")
                                break
                
                # Write the new file
                with open(prices_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['unix_s', 'dist_usd_mwh', 'lmp_usd_mwh'])
                    
                    # Add current hour's data first if it exists
                    if current_hour_row:
                        writer.writerow(current_hour_row)
                        print(f"DEBUG: Added current hour row: {current_hour_row}")
                    
                    # Add new forecast data
                    for i in range(len(price_forecast.dist_list)):
                        writer.writerow([price_forecast.hour_start_s[i], price_forecast.dist_list[i], price_forecast.lmp_list[i]])
                        print(f"DEBUG: Writing row {i}: {price_forecast.hour_start_s[i]} == {datetime.fromtimestamp(price_forecast.hour_start_s[i], tz=pytz.timezone('America/New_York'))} {round(float(price_forecast.dist_list[i]) + float(price_forecast.lmp_list[i]), 2)}")
                print(f"Saved price forecast to {prices_file}")

                return price_forecast
            else:
                raise Exception(f"Failed to receive price forecast from API, status code: {response.status_code}")

    except Exception as e:
        print(f"FAILED to receive price forecast from the price service API and/or to save it to a local CSV: {e}")
        print("Trying to read price forecast from the local CSV file")
        try:
            # Read the local CSV file with the latest received price forecast
            file_path = Path(f"{data_dir}/price_forecast.csv")
            with open(file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)
                rows = list(reader)
            timestamps = [float(row[0]) for row in rows]
            dist_usd_mwh = [float(row[1]) for row in rows]
            lmp_usd_mwh = [float(row[2]) for row in rows]
            reg_usd_mwh = [0.0] * len(rows)

            # Crop the beginning of the CSV and extend the end to get a forecast for the next 48 hours
            time_now = time.time()
            timestamps_forecast = [t for t in timestamps if t > time_now]
            hours_available = len(timestamps_forecast)
            if not hours_available:
                raise Exception("No forecasts available for the next hours!")
            dp_forecast_usd_per_mwh = [p for p,t in zip(dist_usd_mwh, timestamps) if t > time_now]
            lmp_forecast_usd_per_mwh = [p for p,t in zip(lmp_usd_mwh, timestamps) if t > time_now]
            reg_forecast_usd_per_mwh = [p for p,t in zip(reg_usd_mwh, timestamps) if t > time_now]
            if hours_available < 48:
                dp_forecast_usd_per_mwh = dp_forecast_usd_per_mwh + [dp_forecast_usd_per_mwh[-1]] * (48-len(dp_forecast_usd_per_mwh))
                lmp_forecast_usd_per_mwh = lmp_forecast_usd_per_mwh + [lmp_forecast_usd_per_mwh[-1]] * (48-len(lmp_forecast_usd_per_mwh))
                reg_forecast_usd_per_mwh = reg_forecast_usd_per_mwh + [reg_forecast_usd_per_mwh[-1]] * (48-len(reg_forecast_usd_per_mwh))

            # Update the price forecast
            price_forecast = PriceForecast(
                dp_usd_per_mwh=dp_forecast_usd_per_mwh,
                lmp_usd_per_mwh=lmp_forecast_usd_per_mwh,
                reg_usd_per_mwh=reg_forecast_usd_per_mwh,
            )
            print("Successfully read price forecast from local CSV.")
            print(f"- LMP USD/MWh {price_forecast.lmp_usd_per_mwh}")
            print(f"- Total energy USD/MWh {[round(x,2) for x in price_forecast.total_energy]}")
            return price_forecast

        except Exception as e:
            print(f"Could not get a price forecast from the local CSV file: {e}.")
            raise e

async def read_forecasted_price_for_now(data_dir: str = "./data") -> float:
    """Returns the forecasted price for this hour (LMP + Dist) in USD/MWh"""
    try:
        prices_file = Path(f"{data_dir}/price_forecast.csv")
        if prices_file.exists():
            start_of_hour_timestamp = int(time.time()//3600) * 3600
            print(f"DEBUG: start_of_hour_timestamp: {start_of_hour_timestamp} == {datetime.fromtimestamp(start_of_hour_timestamp, tz=pytz.timezone('America/New_York'))}")
            # Read CSV file instead of JSON
            with open(prices_file, 'r', newline='') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                rows = list(reader)
            
            # Find the row with matching timestamp
            for row in rows:
                if float(row[0]) == start_of_hour_timestamp:
                    print("A valid price forecast was available locally.")
                    price = float(row[1]) + float(row[2])  # dist + lmp
                    return price
            
            raise Exception(f"{prices_file} does not have a price forecast for this hour.")
        else:
            raise Exception(f"{prices_file} does not exist.")
    except Exception as e:
        print(f"Failed: {e}")
        return 0








#!/usr/bin/env python3
"""
Test script for the three price functions in minimal_price_client.py
"""

import asyncio
from pathlib import Path

async def test_get_real_time_price():
    """Test the get_real_time_price function"""
    print("=" * 50)
    print("Testing get_real_time_price()")
    print("=" * 50)
    
    try:
        price = await get_real_time_price()
        print(f"✅ Real-time price: ${price:.2f} USD/MWh")
        return price
    except Exception as e:
        print(f"❌ Error getting real-time price: {e}")
        return None


async def test_get_price_forecast_48h():
    """Test the get_price_forecast_48h function"""
    print("\n" + "=" * 50)
    print("Testing get_price_forecast_48h()")
    print("=" * 50)
    
    try:
        forecast: Gw0PriceForecast = await get_price_forecast_48h()
        print(f"✅ Price forecast received successfully!")
        print(f"   - Number of hours: {len(forecast.lmp_list)}")
        print(f"   - First few LMP prices: {forecast.lmp_list[:5]}")
        print(f"   - First few total energy prices: {[round(x, 2) for x in forecast.energy_list[:5]]}")
        return forecast
    except Exception as e:
        print(f"❌ Error getting price forecast: {e}")
        return None


async def test_read_forecasted_price_for_now():
    """Test the read_forecasted_price_for_now function"""
    print("\n" + "=" * 50)
    print("Testing read_forecasted_price_for_now()")
    print("=" * 50)
    
    try:
        price = await read_forecasted_price_for_now()
        if price > 0:
            print(f"✅ Forecasted price for current hour: ${price:.2f} USD/MWh")
        else:
            print("⚠️  No forecast available for current hour (returned 0)")
        return price
    except Exception as e:
        print(f"❌ Error reading forecasted price: {e}")
        return None
        print(f"❌ Error testing PriceForecast model: {e}")
        return None


async def main():
    """Run all tests"""
    print("🚀 Starting tests for price functions...")
    print(f"📁 Working directory: {Path.cwd()}")
        
    # Test the async functions
    # real_time_price = await test_get_real_time_price()
    forecast = await test_get_price_forecast_48h()
    # forecasted_price = await test_read_forecasted_price_for_now()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    tests = [
        # ("Real-time Price", real_time_price is not None and real_time_price > 0),
        ("48h Price Forecast", forecast is not None),
        # ("Current Hour Forecast", forecasted_price is not None)
    ]
    
    passed = sum(1 for _, success in tests if success)
    total = len(tests)
    
    for test_name, success in tests:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")


if __name__ == "__main__":
    asyncio.run(main())
