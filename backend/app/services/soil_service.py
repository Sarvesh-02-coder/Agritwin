# app/services/soil_service.py
import requests
import json
import pandas as pd
from pathlib import Path
from datetime import date
import math

# Paths
CACHE_DIR = Path(__file__).parent.parent / "cache"
DATA_DIR = Path(__file__).resolve().parents[3] / "ml" / "data"

CACHE_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

GEOCODE_URL = "https://nominatim.openstreetmap.org/search"
SOILGRIDS_URL = "https://rest.isric.org/soilgrids/v2.0/properties/query"


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
    """Query SoilGrids API for given lat/lon."""
    params = {
        "lat": lat,
        "lon": lon,
        "depth": "0-5cm",
        "value": "mean",
        "property": ["phh2o", "soc", "sand", "silt", "clay"]
    }
    resp = requests.get(SOILGRIDS_URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def parse_soilgrids(data: dict) -> dict:
    """Extract values safely from SoilGrids JSON."""
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
    """
    Try SoilGrids at lat/lon, expand radius until valid.
    Returns (data, distance_km)
    """
    for r in range(0, max_km + 1, step_km):
        for angle in range(0, 360, 45):
            dx = (r / 111) * math.cos(math.radians(angle))
            dy = (r / 111) * math.sin(math.radians(angle))
            test_lat, test_lon = lat + dy, lon + dx

            raw = query_soilgrids(test_lat, test_lon)
            parsed = parse_soilgrids(raw)

            if parsed:  # ✅ found something
                return parsed, r

    return {}, None


def fetch_soil_data(pincode: str):
    """Fetch soil properties and save CSV."""
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
            raise ValueError(f"❌ No soil data found near pincode {pincode}")

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
            "pH": None,
            "pH_status": "Unknown",
            "organic_carbon_pct": None,
            "sand_pct": None,
            "silt_pct": None,
            "clay_pct": None,
            "soil_texture": "Unknown",
            "note": "No soil data found nearby, pincode must be in a city /urban area."
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
        "note": f"Data taken from {distance_used} km away" if distance_used else "Direct match"
    }


async def get_soil_data(pincode: str):
    return summarize_soil(pincode)


if __name__ == "__main__":
    pin = input("Enter pincode: ")
    print(json.dumps(summarize_soil(pin), indent=2))
