# backend/app/routers/dashboard.py
from fastapi import APIRouter, Query, HTTPException
from typing import Optional, Dict, Any
from app.services.weather_service import fetch_weather_summary
from app.services.crop_service import recommend_crops as _recommend_crops
from app.services.irrigation_service import calculate_irrigation
from app.services.fertilizer_service import get_fertilizer_advice
from app.services.pest_service import get_pest_alerts
from app.models.pydantic_schemas import (
    CropRecommendRequest, IrrigationRequest, FertilizerRequest, PestAlertRequest
)
from app.schemas.response import ResponseModel

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", response_model=ResponseModel)
def get_dashboard(
    pincode: str = Query(..., description="Farmer location pincode"),
    crop: Optional[str] = Query(None, description="Target crop (optional)"),
    area_ha: float = Query(1.0, gt=0, description="Farm area in hectares"),
    soil_pH: Optional[float] = Query(None, description="Soil pH if known"),
    soil_moisture: Optional[float] = Query(None, description="% VWC if known"),
    season: Optional[str] = Query(None, description="kharif/rabi/annual (optional)")
) -> ResponseModel:
    """
    Aggregates quick-preview data for the Dashboard widgets:
    - Weather summary (last 7 days)
    - Crop recommendations (if soil_pH provided)
    - Irrigation preview (weekly)
    - Fertilizer preview (mini-summary)
    - Pest alert snapshot (based on avg weather)
    """
    result: Dict[str, Any] = {
        "weather": None,
        "crop_recommendations": [],
        "irrigation_preview": None,
        "fertilizer_preview": None,
        "pest_preview": {"alerts": []},
        "errors": {}
    }

    try:
        # 1) Weather summary (always required)
        weather = fetch_weather_summary(pincode)
        result["weather"] = weather

        # Extract helper values
        rainfall_7d = weather.get("rainfall_7d_total", 0.0)
        avg_temp = weather.get("temp_7d_avg", 0.0)
        avg_hum = weather.get("humidity_7d_avg", 0.0)

        # 2) Crop recommendations (if soil_pH available)
        if soil_pH is not None:
            try:
                req = CropRecommendRequest(
                    season=season or "kharif",
                    soil_pH=soil_pH,
                    rainfall_mm=rainfall_7d,
                    region=None,
                )
                recs = _recommend_crops(req)
                result["crop_recommendations"] = [r.dict() for r in recs]
            except Exception as e:
                result["errors"]["crop_recommendations"] = str(e)

        # 3) Irrigation preview
        try:
            irr_req = IrrigationRequest(
                crop=crop or "rice",
                area_hectares=area_ha,
                soil_moisture=soil_moisture if soil_moisture is not None else 20.0,
                rainfall_forecast_mm=rainfall_7d,
            )
            irr = calculate_irrigation(irr_req)
            result["irrigation_preview"] = irr.dict()
        except Exception as e:
            result["errors"]["irrigation"] = str(e)

        # 4) Fertilizer preview
        try:
            fert_req = FertilizerRequest(
                crop=crop or "rice",
                area_ha=area_ha,
                season=season or "kharif",
                soil_pH=soil_pH,
                soil_N_level="medium",
                soil_P_level="medium",
                soil_K_level="medium",
                yield_target=None
            )
            fert = get_fertilizer_advice(fert_req)
            result["fertilizer_preview"] = {
                "per_ha_NPK_kg": fert.per_ha_NPK_kg,
                "application_schedule": fert.application_schedule[:2],
                "cautions": fert.cautions[:1],
            }
        except Exception as e:
            result["errors"]["fertilizer"] = str(e)

        # 5) Pest alerts
        try:
            if crop:
                pest_req = PestAlertRequest(
                    crop=crop,
                    season=season or "kharif",
                    temp_c=avg_temp,
                    humidity=avg_hum
                )
                alerts = get_pest_alerts(pest_req)
                result["pest_preview"] = {
                    "alerts": [a.dict() for a in alerts[:3]]
                }
        except Exception as e:
            result["errors"]["pest"] = str(e)

        return ResponseModel(
            success=True,
            message="✅ Dashboard summary generated",
            data=result
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
