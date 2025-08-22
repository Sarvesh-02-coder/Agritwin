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
    resp = requests.get(GEOCODE_URL, params=params, headers={"User-Agent": "AgriTwin/1.0"}, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    if not data:
        raise ValueError(f"❌ Could not find coordinates for pincode {pincode}")

    lat, lon = float(data[0]["lat"]), float(data[0]["lon"])
    return lat, lon


def fetch_weather(pincode: str, days: int = 30):
    """Fetch last N days weather for a given pincode and save as CSV with rolling averages."""

    # Step 1: Convert pincode → lat/lon
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
            "parameters": "T2M,RH2M,PRECTOTCORR,ALLSKY_KT,ALLSKY_SFC_SW_DWN",
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

    # Step 2: Parse NASA response
    params = data["properties"]["parameter"]
    temps = params.get("T2M", {})
    hums = params.get("RH2M", {})
    rains = params.get("PRECTOTCORR", {})
    clearness = params.get("ALLSKY_KT", {})
    solar_rad = params.get("ALLSKY_SFC_SW_DWN", {})

    records = []
    for day in sorted(temps.keys()):
        rad_wm2 = solar_rad.get(day, 0)
        sunlight_hours = (rad_wm2 * 0.024) if rad_wm2 is not None else 0

        records.append({
            "date": pd.to_datetime(day),
            "temperature_C": temps.get(day),
            "humidity_%": hums.get(day),
            "rainfall_mm": rains.get(day),
            "clearness_index": clearness.get(day),
            "solar_radiation_Wm2": rad_wm2,
            "sunlight_hours": round(sunlight_hours, 2)
        })

    df = pd.DataFrame(records).sort_values("date")

    # Rolling 7-day mean
    rolling_cols = ["temperature_C", "humidity_%", "rainfall_mm", "sunlight_hours"]
    for col in rolling_cols:
        df[f"{col}_7d_avg"] = df[col].rolling(window=7, min_periods=1).mean().round(2)

    # Save as CSV
    created_date = date.today().strftime("%Y%m%d")
    csv_path = DATA_DIR / f"weather_{pincode}_{created_date}.csv"
    df.to_csv(csv_path, index=False)

    print(f"✅ Weather data for {pincode} saved to {csv_path}")
    return csv_path


if __name__ == "__main__":
    pincode = input("Enter your pincode: ").strip()
    try:
        fetch_weather(pincode, days=30)
    except Exception as e:
        print(f"❌ Error: {e}")
