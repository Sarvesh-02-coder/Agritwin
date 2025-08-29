# app/services/recommend_service.py

from typing import List, Dict
from app.services import profile_service, soil_service, weather_service

def get_recommendations() -> List[Dict]:
    """
    Generate crop recommendations dynamically using:
    - Active farmer profile
    - Soil data (from soil_service)
    - Weather data (from weather_service)

    Returns a list of recommendations with crop, score, rationale, season, and action.
    """

    # ✅ Get active farmer profile
    profile = profile_service.get_active_profile()
    if not profile:
        return []

    crop_pref = profile.get("crop", None)
    pincode = profile.get("pincode")

    # ✅ Fetch soil data
    soil_data = soil_service.summarize_soil(pincode)
    soil_type = soil_data.get("soil_texture", "loam")
    soil_pH = soil_data.get("pH", 7.0)

    # ✅ Fetch weather data
    weather = weather_service.fetch_weather_summary(pincode)
    rainfall = weather.get("rainfall", 500)   # mm
    season = weather.get("season", "kharif")

    recommendations: List[Dict] = []

    # --- Dynamic recommendation logic ---
    # Base crop preference (from profile)
    if crop_pref:
        recommendations.append({
            "crop": crop_pref,
            "score": 0.95,
            "rationale": f"Farmer preference for {crop_pref} honored",
            "season": season.title(),
            "action": f"Proceed with {crop_pref} planning this season"
        })

    # Soil pH suitability
    if 5.5 <= soil_pH <= 7.0:
        recommendations.append({
            "crop": "Rice",
            "score": 0.85,
            "rationale": f"Neutral pH ({soil_pH}) and {soil_type} soil favor rice",
            "season": "Kharif",
            "action": "Prepare fields for transplanting"
        })
    elif 6.0 <= soil_pH <= 8.0:
        recommendations.append({
            "crop": "Wheat",
            "score": 0.82,
            "rationale": f"Soil pH {soil_pH} supports wheat cultivation",
            "season": "Rabi",
            "action": "Begin land preparation"
        })

    # Rainfall suitability
    if rainfall > 1000:
        recommendations.append({
            "crop": "Sugarcane",
            "score": 0.8,
            "rationale": f"High rainfall ({rainfall} mm) supports sugarcane",
            "season": "Annual",
            "action": "Plan for staggered planting"
        })
    elif 300 <= rainfall <= 900:
        recommendations.append({
            "crop": "Pulses",
            "score": 0.78,
            "rationale": f"Moderate rainfall ({rainfall} mm) ideal for pulses",
            "season": season.title(),
            "action": "Select short-duration pulse varieties"
        })

    # ✅ Always fallback if no match
    if not recommendations:
        recommendations.append({
            "crop": "Millets",
            "score": 0.6,
            "rationale": f"Millets adapt well to {soil_type} soil and variable rainfall",
            "season": season.title(),
            "action": "Use drought-resistant varieties"
        })

    # Sort by score
    recommendations.sort(key=lambda x: x["score"], reverse=True)

    return recommendations[:5]
