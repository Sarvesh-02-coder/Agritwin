# app/services/forecast_service.py

from datetime import date, timedelta
import calendar, random
from typing import List, Dict

from app.services.weather_service import fetch_weather_summary
from app.services.soil_service import summarize_soil
from app.services import profile_service
from app.ml.predict_yield import predict_row
from app.services.market_service import fetch_market_price


CROP_META = {
    "rice":      (120, "Kharif", 2200),
    "wheat":     (120, "Rabi",   2100),
    "maize":     (110, "Kharif", 1800),
    "cotton":    (160, "Kharif", 6000),
    "sugarcane": (300, "Annual", 300),
    "pulses":    (100, "Kharif", 5000),
    "millets":   (90,  "Kharif", 2000),
}


def _guess_meta(crop: str, fallback_price: float):
    duration, season, default_price = CROP_META.get(
        crop.lower(), (120, "Kharif", fallback_price or 2000)
    )
    return duration, season, default_price


def _map_overall_risk(r: float) -> str:
    if r < 15: return "Low"
    if r < 30: return "Medium"
    return "High"


def _risk_from_weather(base_need_mm_week: float, rainfall_7d_total: float) -> float:
    if base_need_mm_week <= 0:
        return 10.0
    frac = max(base_need_mm_week - rainfall_7d_total, 0) / base_need_mm_week
    return min(frac * 40, 40)


def _risk_from_pest(temp: float, hum: float) -> float:
    t = max(0.0, min((temp - 20) / 15, 1.0))
    h = max(0.0, min((hum - 50) / 40, 1.0))
    return min((0.6 * h + 0.4 * t) * 25, 25)


def _risk_from_input_costs(soil_ph: float) -> float:
    if soil_ph is None:
        return 15.0
    return min(abs(soil_ph - 7.0) * 5.0, 25)


def _compute_risk_buckets(crop: str, weather: dict, soil: dict) -> List[Dict]:
    base_need_map = {
        "rice": 50, "wheat": 30, "maize": 35, "sugarcane": 60,
        "cotton": 40, "pulses": 25, "millets": 20
    }
    base_need = base_need_map.get((crop or "").lower(), 30)

    weather_risk = _risk_from_weather(base_need, weather.get("rainfall_7d_total", 0.0))
    pest_risk = _risk_from_pest(
        weather.get("temp_7d_avg", 25.0),
        weather.get("humidity_7d_avg", 60.0),
    )
    input_costs_risk = _risk_from_input_costs(soil.get("pH"))
    market_price_risk = 20.0
    labor_risk = 12.0

    return [
        {"factor": "Weather", "risk": round(weather_risk, 1)},
        {"factor": "Market Price", "risk": market_price_risk},
        {"factor": "Pest/Disease", "risk": round(pest_risk, 1)},
        {"factor": "Input Costs", "risk": round(input_costs_risk, 1)},
        {"factor": "Labor", "risk": labor_risk},
    ]


def generate_forecast() -> dict:
    """
    Generate forecast dynamically from farmer profile (✅ no frontend inputs).
    """
    print("\n===== FORECAST DEBUG LOG =====")

    # 🔹 1. Load Profile
    profile = profile_service.get_active_profile()
    if not profile:
        raise ValueError("No active profile found. Please create or activate a profile.")

    crop = profile.get("crop")
    area_hectares = float(profile.get("area", 1.0))
    pincode = profile.get("pincode")
    state = profile.get("state")
    district = profile.get("district")
    print(f"Profile: crop={crop}, area={area_hectares} ha, location={district}, {state}")

    # 🔹 2. Weather & Soil
    weather = fetch_weather_summary(pincode)
    soil = summarize_soil(pincode)
    print(f"Weather Data: {weather}")
    print(f"Soil Data: {soil}")

    # 🔹 3. Crop Metadata & Market Price
    duration_days, season, default_price = _guess_meta(crop, 2000)
    crop_year = date.today().year

    market_data = fetch_market_price()  # ✅ profile-driven inside service
    price_per_quintal = getattr(market_data, "avg_price", None) or default_price

    print(f"Crop Metadata: duration={duration_days} days, season={season}, price={price_per_quintal} Rs/quintal")

    # 🔹 4. Yield Prediction (with fallback if ML gives 0)
    yield_pred = predict_row(
        state=state,
        district=district,
        crop=crop,
        season=season,
        crop_year=crop_year,
        area=area_hectares,
        production=0.0,   # assume new season
        weather=weather,
        soil=soil,
    )

    if not yield_pred or yield_pred <= 0:
        BASE_YIELD = {
            "rice": 25, "wheat": 20, "maize": 18,
            "cotton": 12, "sugarcane": 80,
            "pulses": 10, "millets": 15
        }
        yield_pred = BASE_YIELD.get(crop.lower(), 15) * area_hectares

    expected_yield = max(yield_pred, 0.0)
    print(f"Predicted Yield (with fallback): {expected_yield:.2f} quintal total")

    # 🔹 5. Income Estimate
    expected_income = expected_yield * price_per_quintal
    print(f"Expected Income: ₹{expected_income:.2f}")

    # 🔹 6. Harvest Date
    sowing_date = date.today()
    harvest_date = sowing_date + timedelta(days=duration_days)
    harvest_date_label = f"{calendar.month_abbr[harvest_date.month]} {harvest_date.year}"
    print(f"Harvest Date: {harvest_date_label}")

    # 🔹 7. Risk Factors
    risk_factors = _compute_risk_buckets(crop, weather, soil)
    overall_risk_pct = sum(r["risk"] for r in risk_factors) / len(risk_factors)
    risk_level = _map_overall_risk(overall_risk_pct)
    print(f"Risk Factors: {risk_factors}")
    print(f"Overall Risk: {overall_risk_pct:.2f}% ({risk_level})")

    # 🔹 8. Yield Timeline (progressive growth curve with randomness)
    yield_forecast = []
    months = max(duration_days // 30, 1)
    for i in range(months):
        month_date = sowing_date + timedelta(days=i * 30)

        # Logistic growth curve (slow start → faster → plateau)
        progress = (i + 1) / months
        yield_pct = 100 * (1 / (1 + pow(2.718, -6 * (progress - 0.5))))

        # ✅ add ±10% randomness
        random_factor = random.uniform(0.9, 1.1)
        yield_pct = yield_pct * random_factor

        monthly_yield = expected_yield * (yield_pct / 100.0)
        monthly_income = monthly_yield * price_per_quintal

        yield_forecast.append({
            "month": calendar.month_abbr[month_date.month],
            "yield": round(monthly_yield, 2),
            "income": round(monthly_income, 2)
        })

    print("Yield Forecast Timeline:", yield_forecast)
    print("===== END DEBUG LOG =====\n")

    return {
        "summary": {
            "expected_yield_qtl": round(expected_yield, 2),
            "expected_income_inr": round(expected_income, 2),
            "harvest_date_label": harvest_date_label,
            "risk_level": risk_level,
            "overall_risk_pct": round(overall_risk_pct, 2)
        },
        "yieldForecast": yield_forecast,
        "riskFactors": risk_factors,
        "marketData": market_data.dict() if hasattr(market_data, "dict") else market_data,
    }
