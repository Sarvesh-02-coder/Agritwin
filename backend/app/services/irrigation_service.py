# app/services/irrigation_service.py
from app.models.pydantic_schemas import IrrigationResponse, IrrigationProfile
from app.services.weather_service import fetch_weather_summary, fetch_weekly_series
import calendar
from datetime import datetime, timedelta

# Approx crop water requirement (mm/week)
CROP_WATER_REQ = {
    "rice": 50,
    "wheat": 30,
    "maize": 35,
    "sugarcane": 60,
    "cotton": 40,
    "pulses": 25,
    "millets": 20
}


def calculate_irrigation(profile: IrrigationProfile) -> IrrigationResponse:
    """
    Compute irrigation needs using:
    - Profile (crop, farmArea, pincode)
    - NASA POWER API (7-day rainfall history)
    """

    # 1. Fetch NASA weather data
    weather_summary = fetch_weather_summary(profile.location)
    weekly_data = fetch_weekly_series(profile.location)

    # 2. Crop base requirement (default = 30 mm/week if crop unknown)
    base_need = CROP_WATER_REQ.get(profile.crop.lower(), 30)

    # 3. Rainfall contribution (total last 7 days)
    rainfall_total = weather_summary.get("rainfall_7d_total", 0.0)

    # 4. Adjust irrigation need (mm) for the whole week
    water_deficit = max(base_need - rainfall_total, 0)

    # 5. Convert mm to liters (1 mm = 10,000 L/hectare)
    liters = water_deficit * profile.farmArea * 10000

    # 6. Add irrigation_mm + short weekday names to each day
    today = datetime.now()
    daily_need = base_need / 7  # mm/day requirement

    for i, day in enumerate(weekly_data):
        weekday_idx = (today + timedelta(days=i)).weekday()
        day["day_name"] = calendar.day_abbr[weekday_idx]  # e.g. "Mon", "Tue"

        rainfall = day.get("rainfall_mm", 0)
        irrigation = max(daily_need - rainfall, 0)

        day["irrigation_mm"] = round(irrigation, 2)

    # 7. Build response
    return IrrigationResponse(
        water_needed_mm=round(water_deficit, 2),
        water_needed_liters=round(liters, 2),
        rationale=(
            f"{profile.crop} requires ~{base_need} mm/week. "
            f"Rainfall over last 7 days ({rainfall_total:.1f} mm) reduces net irrigation need."
        ),
        weather_summary=weather_summary,
        weather_weekly=weekly_data
    )
