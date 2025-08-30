import os
import requests
import json
import pandas as pd
from pathlib import Path
from datetime import date
import math
from dotenv import load_dotenv

# --- Base directories ---
BASE_DIR = Path(__file__).resolve().parent      # app/services
BACKEND_ROOT = BASE_DIR.parents[2]             # backend root
CACHE_DIR = BACKEND_ROOT / "cache"
DATA_DIR = BACKEND_ROOT / "ml" / "data"

CACHE_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# --- Load centralized .env ---
ENV_PATH = BACKEND_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# --- API URLs from .env ---
GEOCODE_URL = os.getenv("GEOCODE_URL", "https://nominatim.openstreetmap.org/search")
SOILGRIDS_URL = os.getenv("SOILGRIDS_URL", "https://rest.isric.org/soilgrids/v2.0/properties/query")

# ✅ fallback soil values (safe defaults)
DEFAULT_SOIL = {
    "phh2o": 7.0,
    "soc": 0.75,
    "sand": 40,
    "silt": 40,
    "clay": 20,
    "_distance_km": None,
    "_note": "Default soil data used (SoilGrids unavailable)"
}


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
    return float(data[0]["lat"]), float(data[0]["lon"])


def query_soilgrids(lat: float, lon: float):
    """Query SoilGrids API for given lat/lon with error handling."""
    params = {
        "lat": lat,
        "lon": lon,
        "depth": "0-5cm",
        "value": "mean",
        "property": ["phh2o", "soc", "sand", "silt", "clay"]
    }
    try:
        resp = requests.get(SOILGRIDS_URL, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        if resp.status_code == 429:
            return None
        raise e
    except Exception:
        return None


def parse_soilgrids(data: dict) -> dict:
    """Extract values safely from SoilGrids JSON."""
    if not data:
        return {}
    result = {}
    for layer in data.get("properties", {}).get("layers", []):
        name = layer.get("name")
        depths = layer.get("depths", [])
        if not depths:
            continue
        values = depths[0].get("values", {})
        mean_val = values.get("mean")
        if mean_val is not None:
            result[name] = mean_val
    return result


def fetch_with_fallback(lat, lon, max_km=20, step_km=2):
    """Try SoilGrids at lat/lon, expand radius until valid. Returns (data, distance_km)."""
    for r in range(0, max_km + 1, step_km):
        for angle in range(0, 360, 45):
            dx = (r / 111) * math.cos(math.radians(angle))
            dy = (r / 111) * math.sin(math.radians(angle))
            test_lat, test_lon = lat + dy, lon + dx

            raw = query_soilgrids(test_lat, test_lon)
            parsed = parse_soilgrids(raw)

            if parsed:
                return parsed, r
    return {}, None


def fetch_soil_data(pincode: str):
    """Fetch soil properties and save CSV, fallback to defaults if needed."""
    lat, lon = get_latlon_from_pincode(pincode)
    created_date = date.today().strftime("%Y%m%d")

    cache_file = CACHE_DIR / f"soil_{pincode}_{created_date}.json"
    if cache_file.exists():
        with open(cache_file, "r") as f:
            parsed = json.load(f)
        distance_used = parsed.get("_distance_km", None)
    else:
        parsed, distance_used = fetch_with_fallback(lat, lon)
        if not parsed:
            parsed = DEFAULT_SOIL.copy()
            distance_used = None

        parsed["_distance_km"] = distance_used
        with open(cache_file, "w") as f:
            json.dump(parsed, f)

    df = pd.DataFrame([parsed])
    csv_path = DATA_DIR / f"soil_{pincode}_{created_date}.csv"
    df.to_csv(csv_path, index=False)

    print(f"✅ Soil data for {pincode} saved to {csv_path}")
    return csv_path


def summarize_soil(pincode: str) -> dict:
    """Summarize soil info for frontend display."""
    created_date = date.today().strftime("%Y%m%d")
    csv_path = DATA_DIR / f"soil_{pincode}_{created_date}.csv"

    if not csv_path.exists():
        fetch_soil_data(pincode)

    df = pd.read_csv(csv_path)
    row = df.iloc[0].to_dict()

    ph = row.get("phh2o")
    soc = row.get("soc")
    sand = row.get("sand")
    silt = row.get("silt")
    clay = row.get("clay")
    distance_used = row.get("_distance_km")

    if pd.isna(ph):
        return {
            "pH": DEFAULT_SOIL["phh2o"],
            "pH_status": "Neutral",
            "organic_carbon_pct": DEFAULT_SOIL["soc"],
            "sand_pct": DEFAULT_SOIL["sand"],
            "silt_pct": DEFAULT_SOIL["silt"],
            "clay_pct": DEFAULT_SOIL["clay"],
            "soil_texture": "Loamy",
            "note": "Default soil data used (SoilGrids unavailable)"
        }

    ph = round(float(ph), 1)
    soc = round(float(soc), 2) if soc is not None else None

    if sand is not None and sand > 70:
        texture = "Sandy"
    elif clay is not None and clay > 35:
        texture = "Clayey"
    else:
        texture = "Loamy"

    if ph < 5.5:
        ph_status = "Strongly acidic"
    elif 5.5 <= ph < 6.5:
        ph_status = "Moderately acidic"
    elif 6.5 <= ph <= 7.5:
        ph_status = "Neutral"
    elif 7.5 < ph <= 8.5:
        ph_status = "Slightly alkaline"
    else:
        ph_status = "Strongly alkaline"

    return {
        "pH": ph,
        "pH_status": ph_status,
        "organic_carbon_pct": soc,
        "sand_pct": sand,
        "silt_pct": silt,
        "clay_pct": clay,
        "soil_texture": texture,
        "note": f"Data taken from {distance_used} km away" if distance_used else "Direct match or default"
    }


async def get_soil_data(pincode: str):
    return summarize_soil(pincode)


if __name__ == "__main__":
    pin = input("Enter pincode: ")
    print(json.dumps(summarize_soil(pin), indent=2))
