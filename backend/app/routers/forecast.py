# app/routers/forecast.py
from fastapi import APIRouter, HTTPException
from app.services import forecast_service, profile_service
from app.schemas.response import ResponseModel   # ✅ unified response schema

router = APIRouter(prefix="/forecast", tags=["Forecast"])


@router.get("/", response_model=ResponseModel)
def get_forecast():
    """
    Generate crop forecast using active saved profile + weather + soil + mandi price.
    """
    try:
        # 🔹 Load active profile
        profile = profile_service.get_active_profile()
        if not profile:
            raise HTTPException(status_code=404, detail="No active profile found")

        # 🔹 Generate forecast (auto-uses profile inside forecast_service)
        forecast = forecast_service.generate_forecast()

        return ResponseModel(
            success=True,
            data={
                "profile": profile,   # ✅ return full profile dict
                "forecast": forecast  # ✅ includes summary, yieldForecast, riskFactors, marketData
            },
            message=f"Forecast generated successfully for {profile.get('crop', 'Unknown Crop')}"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
