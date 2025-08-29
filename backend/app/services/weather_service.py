# app/services/weather_service.py
import requests
import json
import pandas as pd
from pathlib import Path
from datetime import date, timedelta

# Paths
CACHE_DIR = Path(__file__).parent.parent / "cache"
DATA_DIR = Path(__file__).resolve().parents[3] / "ml" / "data"

CACHE_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
GEOCODE_URL = "https://nominatim.openstreetmap.org/search"


def get_latlon_from_pincode(pincode: str):
    """Convert pincode → (lat, lon) using OpenStreetMap Nominatim."""
    params = {
        "postalcode": pincode,
        "country": "India",
        "format": "json",
        "limit": 1
    }
    resp = requests.get(
        GEOCODE_URL, params=params,
        headers={"User-Agent": "AgriTwin/1.0"}, timeout=20
    )
    resp.raise_for_status()
    data = resp.json()

    if not data:
        raise ValueError(f"❌ Could not find coordinates for pincode {pincode}")

    lat, lon = float(data[0]["lat"]), float(data[0]["lon"])
    return lat, lon


def fetch_weather(pincode: str, days: int = 30):
    """
    Fetch last N days weather (rainfall, temp, humidity, sunlight) for given pincode.
    Uses NASA POWER API. Caches raw JSON and stores parsed CSV.
    Returns: CSV path.
    """
    lat, lon = get_latlon_from_pincode(pincode)

    today = date.today()
    end = today - timedelta(days=1)
    start = end - timedelta(days=days - 1)

    cache_file = CACHE_DIR / f"weather_{pincode}_{start}_{end}.json"
    if cache_file.exists():
        with open(cache_file, "r") as f:
            data = json.load(f)
    else:
        params = {
            "parameters": "T2M,RH2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN",
            "start": start.strftime("%Y%m%d"),
            "end": end.strftime("%Y%m%d"),
            "latitude": lat,
            "longitude": lon,
            "format": "JSON",
            "community": "AG"
        }

        resp = requests.get(BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        with open(cache_file, "w") as f:
            json.dump(data, f)

    # Extract NASA data
    params = data["properties"]["parameter"]
    temps = params.get("T2M", {})
    hums = params.get("RH2M", {})
    rains = params.get("PRECTOTCORR", {})
    solar = params.get("ALLSKY_SFC_SW_DWN", {})

    records = []
    for day in sorted(temps.keys()):
        temp_val = temps.get(day, 0)
        hum_val = hums.get(day, 0)
        rain_val = rains.get(day, 0)
        solar_val = solar.get(day, 0)

        temp_val = 0 if temp_val == -999 else temp_val
        hum_val = 0 if hum_val == -999 else hum_val
        rain_val = 0 if rain_val == -999 else rain_val
        solar_val = 0 if solar_val == -999 else solar_val

        # Approx sunlight hours = MJ/m²/day ÷ 0.5
        sunlight_hours = round(solar_val / 0.5, 1)

        records.append({
            "date": pd.to_datetime(day).strftime("%Y-%m-%d"),
            "temperature_C": temp_val,
            "humidity_pct": hum_val,
            "rainfall_mm": rain_val,
            "sunlight_hours": sunlight_hours,
        })

    df = pd.DataFrame(records).sort_values("date")

    # ✅ Ensure all expected columns exist
    for col in ["temperature_C", "humidity_pct", "rainfall_mm", "sunlight_hours"]:
        if col not in df.columns:
            df[col] = 0

    # Save as CSV
    created_date = date.today().strftime("%Y%m%d")
    csv_path = DATA_DIR / f"weather_{pincode}_{created_date}.csv"
    df.to_csv(csv_path, index=False)

    print(f"✅ Weather data for {pincode} saved to {csv_path}")
    return csv_path


def fetch_weather_summary(pincode: str) -> dict:
    """
    Summarize last 7 days weather.
    Returns rainfall total, avg temp, avg humidity.
    """
    created_date = date.today().strftime("%Y%m%d")
    csv_path = DATA_DIR / f"weather_{pincode}_{created_date}.csv"

    if not csv_path.exists():
        fetch_weather(pincode, days=30)

    df = pd.read_csv(csv_path, parse_dates=["date"])
    last7 = df.tail(7)

    return {
        "rainfall_7d_total": round(last7["rainfall_mm"].sum(), 1),
        "temp_7d_avg": round(last7["temperature_C"].mean(), 1),
        "humidity_7d_avg": round(last7["humidity_pct"].mean(), 1),
    }


def fetch_weekly_series(pincode: str) -> list:
    """
    Returns last 7 days of weather data formatted for frontend.
    """
    created_date = date.today().strftime("%Y%m%d")
    csv_path = DATA_DIR / f"weather_{pincode}_{created_date}.csv"

    if not csv_path.exists():
        fetch_weather(pincode, days=30)

    df = pd.read_csv(csv_path, parse_dates=["date"])
    last7 = df.tail(7).copy()

    result = []
    for _, row in last7.iterrows():
        result.append({
            "date": row["date"].strftime("%Y-%m-%d"),
            "temperature_C": round(float(row["temperature_C"]), 1),
            "humidity_pct": round(float(row["humidity_pct"]), 1),
            "rainfall_mm": round(float(row["rainfall_mm"]), 1),
            "sunlight_hours": round(float(row["sunlight_hours"]), 1),
        })

    return result


async def get_weather_data(pincode: str):
    """
    Fetch summary + weekly series for irrigation service.
    """
    summary = fetch_weather_summary(pincode)
    weekly = fetch_weekly_series(pincode)
    return summary, weekly


def fetch_weather_features(pincode: str) -> dict:
    """
    Fetch processed weather features for recommendation and pest services.
    Uses the last 7 days summary.
    Returns: dict with avg temp, avg humidity, total rainfall, avg sunlight.
    """
    created_date = date.today().strftime("%Y%m%d")
    csv_path = DATA_DIR / f"weather_{pincode}_{created_date}.csv"

    if not csv_path.exists():
        fetch_weather(pincode, days=30)

    df = pd.read_csv(csv_path, parse_dates=["date"])
    last7 = df.tail(7)

    return {
        "avg_temp": round(last7["temperature_C"].mean(), 1),
        "avg_humidity": round(last7["humidity_pct"].mean(), 1),
        "total_rainfall": round(last7["rainfall_mm"].sum(), 1),
        "avg_sunlight": round(last7["sunlight_hours"].mean(), 1),
    }
