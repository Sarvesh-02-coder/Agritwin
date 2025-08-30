# app/ml/inference.py
import joblib
from pathlib import Path
import pandas as pd

# Import services
from app.services.profile_service import get_active_profile
from app.services.weather_service import fetch_weather_summary, fetch_weekly_series
from app.services.soil_service import summarize_soil
from app.services.irrigation_service import calculate_irrigation
from app.ml.predict_yield import predict_row

from app.models.pydantic_schemas import WhatIfRequest

MODEL_PATH = Path(__file__).resolve().parents[0] / "artifacts" / "yield_model.pkl"

# Load trained model (predict_row will also ensure model exists via _ensure_model)
if not MODEL_PATH.exists():
    # We don't crash here since predict_row does its own check; but we log for clarity
    print("⚠ Model path not present at inference.py level; predict_row will check model.")


def predict_yield():
    """
    Legacy helper: uses active profile to predict yield (existing behavior).
    Kept unchanged for existing calls.
    """
    profile = get_active_profile()
    if not profile:
        raise RuntimeError("❌ No active profile found. Please set a profile first.")

    pincode = profile.get("pincode")
    crop = profile.get("primary_crop")
    farm_area = profile.get("farm_area")

    # Fetch data from services
    weather = fetch_weather_summary(pincode)
    soil = summarize_soil(pincode)

    # Updated: irrigation now expects an IrrigationProfile-like object
    try:
        from app.models.pydantic_schemas import IrrigationProfile
        irrigation_profile = IrrigationProfile(crop=crop, farmArea=farm_area, location=pincode)
        irrigation = calculate_irrigation(irrigation_profile)
    except Exception as e:
        irrigation = {"error": f"Could not compute irrigation: {str(e)}"}

    # Build feature vector by delegating to predict_row
    predicted_yield = predict_row(
        state=profile.get("state", "Unknown"),
        district=profile.get("district", "Unknown"),
        crop=crop,
        season="Kharif",
        crop_year=2024,
        area=farm_area,
        production=0.0,
        weather=weather,
        soil=soil,
    )

    return {
        "profile": profile,
        "weather": weather,
        "soil": soil,
        "irrigation": irrigation,
        "predicted_yield": float(predicted_yield)
    }


def what_if_yield(request: WhatIfRequest):
    ...
    # Predict baseline
    predicted = predict_row(
        state=(profile.get("state") if profile else "Unknown"),
        district=(profile.get("district") if profile else "Unknown"),
        crop=crop,
        season=request.season or "Kharif",
        crop_year=2024,
        area=area,
        production=0.0,
        weather=weather,
        soil=soil,
    )

    # ✅ Post-hoc adjustments using penalty factors
    sowing_delay = request.sowing_delay or 0
    irrigation_delay = request.irrigation_delay or 0

    # Apply multiplicative penalties instead of flat subtraction
    delay_penalty = 1 - (0.05 * sowing_delay) - (0.03 * irrigation_delay)
    delay_penalty = max(0.2, delay_penalty)  # ensure yield doesn’t go negative/unrealistic

    adjusted_predicted = float(predicted) * delay_penalty

    # Compute irrigation
    try:
        from app.models.pydantic_schemas import IrrigationProfile
        irrigation_profile = IrrigationProfile(crop=crop, farmArea=area, location=pincode or "000000")
        irrigation = calculate_irrigation(irrigation_profile)
    except Exception as e:
        irrigation = {"error": f"Could not compute irrigation: {str(e)}"}

    # ✅ Dynamic Growth curve
    import math, random
    weeks = 10
    growth_curve = []
    for i in range(1, weeks + 1):
        frac = 1 / (1 + math.exp(-0.8 * (i - weeks / 2)))  # logistic curve
        val = adjusted_predicted * frac
        val += random.uniform(-2, 2)  # add small noise
        val = round(max(0.0, val), 2)
        growth_curve.append({"week": f"Week {i}", "yield": val})

    return {
        "predicted_yield": round(adjusted_predicted, 2),
        "weather": weather,
        "soil": soil,
        "irrigation": irrigation,
        "growth_curve": growth_curve,
        "input_overrides": request.dict(by_alias=True)
    }
