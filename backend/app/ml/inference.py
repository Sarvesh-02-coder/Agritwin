from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path
import requests

# ----------------------------
# Paths (relative to backend/app/ml)
# ----------------------------
ROOT_DIR = Path(__file__).resolve().parent
MODEL_PATH = ROOT_DIR / "artifacts" / "yield_model.pkl"
CACHE_PATH = ROOT_DIR / "artifacts" / "soil_cache.csv"

# ----------------------------
# Load model
# ----------------------------
model = joblib.load(MODEL_PATH)

# ----------------------------
# FastAPI app
# ----------------------------
app = FastAPI(title="AgriTwin Yield Prediction API")

# ----------------------------
# Request schema
# ----------------------------
class YieldRequest(BaseModel):
    soil_moisture_: float
    soil_pH: float
    temperature_C: float
    rainfall_mm: float
    humidity_: float
    sunlight_hours: float
    crop_type: str
    irrigation_type: str
    fertilizer_type: str
    NDVI_index: float
    total_days: int
    region: str
    crop_disease_status: str
    growing_season_length: int
    lat: float
    lon: float
    refresh_soil: bool = False  # force refresh SoilGrids


# ----------------------------
# SoilGrids fetch
# ----------------------------
def fetch_soilgrids_data(lat, lon):
    url = f"https://rest.soilgrids.org/query?lon={lon}&lat={lat}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return {}
        data = response.json()
        soil = data["properties"]["layers"]
        return {
            "soil_ph_sg": soil["phh2o"]["depths"][0]["values"]["mean"],
            "organic_carbon": soil["soc"]["depths"][0]["values"]["mean"],
            "sand_fraction": soil["sand"]["depths"][0]["values"]["mean"],
            "clay_fraction": soil["clay"]["depths"][0]["values"]["mean"],
            "silt_fraction": soil["silt"]["depths"][0]["values"]["mean"],
        }
    except:
        return {}


# ----------------------------
# Cache manager
# ----------------------------
def get_soil_features(lat, lon, refresh=False):
    if CACHE_PATH.exists():
        cache = pd.read_csv(CACHE_PATH)
    else:
        cache = pd.DataFrame(columns=[
            "lat", "lon", "soil_ph_sg", "organic_carbon",
            "sand_fraction", "clay_fraction", "silt_fraction"
        ])

    # Look up in cache
    row = cache[(cache["lat"] == lat) & (cache["lon"] == lon)]

    if not row.empty and not refresh:
        return row.iloc[0].to_dict()

    # Fetch fresh data
    features = fetch_soilgrids_data(lat, lon)
    features.update({"lat": lat, "lon": lon})

    # Update cache
    cache = pd.concat([
        cache[~((cache["lat"] == lat) & (cache["lon"] == lon))],
        pd.DataFrame([features])
    ], ignore_index=True)

    cache.to_csv(CACHE_PATH, index=False)

    return features


# ----------------------------
# Prediction endpoint
# ----------------------------
@app.post("/predict_yield")
def predict_yield(req: YieldRequest):
    soil_features = get_soil_features(req.lat, req.lon, refresh=req.refresh_soil)

    data = pd.DataFrame([{
        "soil_moisture_%": req.soil_moisture_,
        "soil_pH": req.soil_pH,
        "temperature_C": req.temperature_C,
        "rainfall_mm": req.rainfall_mm,
        "humidity_%": req.humidity_,
        "sunlight_hours": req.sunlight_hours,
        "crop_type": req.crop_type,
        "irrigation_type": req.irrigation_type,
        "fertilizer_type": req.fertilizer_type,
        "NDVI_index": req.NDVI_index,
        "total_days": req.total_days,
        "region": req.region,
        "crop_disease_status": req.crop_disease_status,
        "growing_season_length": req.growing_season_length,
        **soil_features
    }])

    pred = model.predict(data)[0]
    return {"predicted_yield": round(float(pred), 2)}
