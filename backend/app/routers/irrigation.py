# app/routers/irrigation.py

from fastapi import APIRouter, HTTPException
from app.models.pydantic_schemas import IrrigationResponse, IrrigationProfile
from app.services.irrigation_service import calculate_irrigation
from app.services.profile_service import get_active_profile   # ✅ use new helper

router = APIRouter(prefix="/irrigation", tags=["Irrigation"])


@router.get("/", response_model=IrrigationResponse)
def get_irrigation_advice():
    """
    Endpoint to calculate irrigation requirement using the active profile.
    Active profile = profile with `"active": true` in profiles.json.
    """
    try:
        active_profile = get_active_profile()
        if not active_profile:
            raise HTTPException(status_code=404, detail="No active profile found")

        result = calculate_irrigation(IrrigationProfile(**active_profile))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
