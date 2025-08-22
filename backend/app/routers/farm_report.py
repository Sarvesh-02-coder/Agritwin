# backend/app/routers/farm_report.py
from fastapi import APIRouter
from typing import Optional, Dict, Any
from app.services import advisors, market_service

router = APIRouter(prefix="/farm-report", tags=["farm-report"])

@router.post("")
def farm_report(
    soil_pH: Optional[float] = None,
    rainfall_mm_7d: Optional[float] = None,
    season: Optional[str] = None,
    soil_moisture: Optional[float] = None,
    n: Optional[float] = None,
    p: Optional[float] = None,
    k: Optional[float] = None,
    crop: Optional[str] = None,
    temp_c: Optional[float] = None,
    humidity_pct: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Aggregated farm advisory report.
    Combines crop recommendation, irrigation, fertilizer, pest, and market services.
    """

    # Use advisors.py (your rule-based services)
    crop_recos = advisors.recommend_crops(soil_pH, rainfall_mm_7d, season)
    irrigation = advisors.irrigation_advice(soil_moisture, rainfall_mm_7d, crop)
    fert = advisors.fertilizer_recommendation(n, p, k, crop, soil_pH)
    pests = advisors.pest_alerts(crop, temp_c, humidity_pct, season)

    # Market price service (fallback = no data)
    try:
        market = market_service.fetch_market_price(
            {"commodity": crop, "state": None, "district": None}
        )
    except Exception:
        market = {"status": "no data"}

    return {
        "crop_recommendations": crop_recos,
        "irrigation": irrigation,
        "fertilizer": fert,
        "pest_alerts": pests,
        "market": market,
    }
