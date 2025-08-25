# backend/app/routers/farm_report.py
from fastapi import APIRouter
from app.services import advisors, market_service
from app.schemas.response import FarmReportResponse
from app.models.pydantic_schemas import FarmReportRequest

router = APIRouter(prefix="/farm-report", tags=["farm-report"])

@router.post("/", response_model=FarmReportResponse)
def farm_report(req: FarmReportRequest) -> FarmReportResponse:
    """
    Aggregated farm advisory report.
    Combines crop recommendation, irrigation, fertilizer, pest, and market services.
    """

    # Use advisors.py (rule-based services)
    crop_recos = advisors.recommend_crops(req.soil_pH, req.rainfall_mm_7d, req.season)
    irrigation = advisors.irrigation_advice(req.soil_moisture, req.rainfall_mm_7d, req.crop)
    fert = advisors.fertilizer_recommendation(req.n, req.p, req.k, req.crop, req.soil_pH)
    pests = advisors.pest_alerts(req.crop, req.temp_c, req.humidity_pct, req.season)

    # Market price service
    try:
        market = market_service.fetch_market_price(
            {"commodity": req.crop, "state": None, "district": None}
        )
    except Exception:
        market = {"status": "no data"}

    return FarmReportResponse(
        crop_recommendations=crop_recos,
        irrigation=irrigation,
        fertilizer=fert,
        pest_alerts=pests,
        market=market,
    )
