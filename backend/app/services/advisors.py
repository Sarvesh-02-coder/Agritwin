# backend/app/services/advisors.py
from typing import List, Dict, Any, Optional

def recommend_crops(soil_pH: Optional[float],
                    rainfall_mm_7d: Optional[float],
                    season: Optional[str]) -> List[Dict[str, Any]]:
    recos = []
    pH = soil_pH if soil_pH is not None else 6.8
    rain = rainfall_mm_7d if rainfall_mm_7d is not None else 20.0
    szn = (season or "").lower()

    # Example India-oriented rules (tweak freely)
    if 6.0 <= pH <= 7.5 and rain >= 15 and ("kharif" in szn or not szn):
        recos.append({"crop": "Rice", "why": "Neutral pH and adequate rain in Kharif."})
    if 6.0 <= pH <= 7.8 and rain <= 30 and ("rabi" in szn or not szn):
        recos.append({"crop": "Wheat", "why": "Neutral–slightly alkaline pH; moderate water."})
    if pH >= 7.0 and rain <= 25:
        recos.append({"crop": "Cotton", "why": "Tolerates slightly alkaline soils; low–moderate rainfall."})
    if 5.5 <= pH <= 7.0 and rain >= 10:
        recos.append({"crop": "Maize", "why": "Wide pH tolerance and moderate rainfall."})

    return recos[:4] or [{"crop": "Maize", "why": "Generalist fallback."}]


def irrigation_advice(soil_moisture: Optional[float],
                      rainfall_mm_7d: Optional[float],
                      crop: Optional[str]) -> Dict[str, Any]:
    sm = soil_moisture if soil_moisture is not None else 25.0   # %
    rain = rainfall_mm_7d if rainfall_mm_7d is not None else 20.0
    crop = (crop or "generic").lower()

    # crude weekly water need (mm)
    base_need_mm = 35 if crop in ["rice"] else 20
    rain_credit = min(rain, base_need_mm * 0.7)
    net_mm = max(base_need_mm - rain_credit, 0)

    # moisture buffer
    if sm > 35:
        net_mm *= 0.5
    elif sm < 15:
        net_mm *= 1.2

    return {
        "recommended_irrigation_mm_this_week": round(net_mm, 1),
        "notes": f"Soil moisture {sm}%, recent rain {rain} mm."
    }


def fertilizer_recommendation(n: Optional[float], p: Optional[float], k: Optional[float],
                              crop: Optional[str], soil_pH: Optional[float]) -> Dict[str, Any]:
    crop = (crop or "Generic").lower()
    n = n if n is not None else 0.0
    p = p if p is not None else 0.0
    k = k if k is not None else 0.0
    pH = soil_pH if soil_pH is not None else 6.8

    # very simple “gap to target” logic (illustrative only)
    need_n = 100 - n if n < 100 else 0
    need_p = 60 - p if p < 60 else 0
    need_k = 60 - k if k < 60 else 0

    note = None
    if pH < 5.5:
        note = "Soil acidic: consider liming."
    elif pH > 8.0:
        note = "Soil alkaline: split N doses; use SSP for P."

    return {
        "N_required_kg_ha": max(round(need_n, 1), 0),
        "P_required_kg_ha": max(round(need_p, 1), 0),
        "K_required_kg_ha": max(round(need_k, 1), 0),
        "notes": note
    }


def pest_alerts(crop: Optional[str],
                temp_c: Optional[float],
                humidity_pct: Optional[float],
                season: Optional[str]) -> List[Dict[str, Any]]:
    crop = (crop or "").lower()
    t = temp_c if temp_c is not None else 28.0
    h = humidity_pct if humidity_pct is not None else 70.0
    alerts = []

    if "rice" in crop and h >= 75 and 24 <= t <= 32:
        alerts.append({"pest": "Brown planthopper", "risk": "High", "why": "Warm & humid."})
    if "wheat" in crop and 15 <= t <= 25 and h >= 70:
        alerts.append({"disease": "Rust", "risk": "Medium", "why": "Cool & humid."})
    if "cotton" in crop and t >= 25 and h <= 60:
        alerts.append({"pest": "Whitefly", "risk": "Medium", "why": "Warm & dry."})

    return alerts or [{"note": "No specific alerts based on current conditions."}]


def get_market_prices(crop: Optional[str]) -> Dict[str, Any]:
    if not crop:
        return {"status": "skipped", "note": "Provide crop to fetch prices."}
    # Placeholder; wire to Agmarknet later.
    return {
        "status": "placeholder",
        "crop": crop,
        "recent_avg_price_rs_per_qtl": None,
        "note": "Integrate Agmarknet API later."
    }
