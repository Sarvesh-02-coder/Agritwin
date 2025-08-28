# app/ml/inference.py
import joblib
from pathlib import Path
import pandas as pd

# Import services
from app.services.profile_service import get_active_profile
from app.services.weather_service import fetch_weather_summary
from app.services.soil_service import summarize_soil
from app.services.irrigation_service import calculate_irrigation

MODEL_PATH = Path(__file__).resolve().parents[0] / "artifacts" / "yield_model.pkl"

# Load trained model
if not MODEL_PATH.exists():
    raise RuntimeError("❌ Model not found. Please train it first using train_yield.py")

model = joblib.load(MODEL_PATH)
print(f"✅ Model loaded from {MODEL_PATH}")

def predict_yield():
    profile = get_active_profile()
    if not profile:
        raise RuntimeError("❌ No active profile found. Please set a profile first.")

    pincode = profile.get("pincode")
    crop = profile.get("primary_crop")
    farm_area = profile.get("farm_area")

    # Fetch data from services
    weather = fetch_weather_summary(pincode)
    soil = summarize_soil(pincode)
    irrigation = calculate_irrigation(crop, farm_area, pincode)

    # Build feature vector
    features = {
        "State": profile.get("state", "Unknown"),
        "District": profile.get("district", "Unknown"),
        "Crop": crop,
        "Crop_Year": 2024,   # can be dynamic
        "Season": "Kharif",  # can be based on profile/weather
        "Area": farm_area,
        "Production": 0,     # placeholder, since we predict Yield

        # Extra features
        "rainfall_7d_total": weather.get("rainfall_7d_total", 0),
        "temp_7d_avg": weather.get("temp_7d_avg", 0),
        "humidity_7d_avg": weather.get("humidity_7d_avg", 0),
        "soil_ph": soil.get("pH", 0),
        "soil_soc": soil.get("organic_carbon_pct", 0),
        "soil_sand": soil.get("sand_pct", 0),
        "soil_silt": soil.get("silt_pct", 0),
        "soil_clay": soil.get("clay_pct", 0),
        "water_needed_mm": irrigation.get("water_needed_mm", 0),
        "water_needed_liters": irrigation.get("water_needed_liters", 0),
    }

    df = pd.DataFrame([features])

    # Predict yield
    predicted_yield = model.predict(df)[0]

    return {
        "profile": profile,
        "weather": weather,
        "soil": soil,
        "irrigation": irrigation,
        "predicted_yield": float(predicted_yield)
    }
