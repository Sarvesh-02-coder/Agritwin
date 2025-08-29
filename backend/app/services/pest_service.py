# app/services/pest_service.py

import pandas as pd
from pathlib import Path
from app.services import profile_service, weather_service

# Path to dataset
DATA_PATH = Path(__file__).resolve().parents[1] / "ml" / "data" / "pest_disease.csv"

# Load dataset once at startup
try:
    df = pd.read_csv(DATA_PATH)
    print(f"✅ Pest dataset loaded: {len(df)} rows")
except Exception as e:
    print(f"❌ Error loading pest dataset: {e}")
    df = pd.DataFrame()  # fallback


def get_pest_alerts():
    """
    Generate pest and disease alerts dynamically using:
    - Active profile (crop, season)
    - Weather service (temperature, humidity)
    """

    profile = profile_service.get_active_profile()
    if not profile:
        return [{
            "pest": None,
            "disease": None,
            "risk": "low",
            "note": "No active profile found"
        }]

    crop = profile.get("crop", "").lower()
    season = profile.get("season", "").lower() or "kharif"  # ✅ fallback

    # Get current weather
    weather = weather_service.fetch_weather_summary(profile.get("pincode"))
    temp = weather.get("temperature") if weather else None
    humidity = weather.get("humidity") if weather else None

    # ✅ Fallback weather
    if temp is None:
        temp = 30
    if humidity is None:
        humidity = 80

    if df.empty:
        return [{
            "pest": None,
            "disease": None,
            "risk": "low",
            "note": "Pest dataset not available"
        }]

    alerts = []

    for _, row in df.iterrows():
        row_crop = str(row.get("crop", "")).lower()
        row_season = str(row.get("season", "")).lower()

        if row_crop != crop:
            continue

        if row_season != season:
            continue

        if not (row["temp_min"] <= temp <= row["temp_max"]):
            continue

        if not (row["humidity_min"] <= humidity <= row["humidity_max"]):
            continue

        # ✅ All matched → high risk alert
        alerts.append({
            "pest": row.get("pest"),
            "disease": row.get("disease"),
            "risk": "high",
            "note": f"In this season, {row.get('note', '')}"
        })

    # If nothing matched, return safe default
    if not alerts:
        alerts.append({
            "pest": None,
            "disease": None,
            "risk": "low",
            "note": f"In this season, no major pest/disease risks detected for {crop}"
        })

    return alerts
