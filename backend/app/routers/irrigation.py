from fastapi import APIRouter
from pydantic import BaseModel
from app.schemas.response import ResponseModel

router = APIRouter(
    prefix="/irrigation",
    tags=["Irrigation Recommendation"]
)

# Input schema
class IrrigationRequest(BaseModel):
    soil_moisture: float  # %
    rainfall_mm: float    # recent rainfall (mm)
    crop: str
    season: str           # kharif, rabi, summer
    evapotranspiration: float  # mm/day, if available (else 0)

# Approximate crop water requirement per day (mm/day)
CROP_WATER_REQUIREMENT = {
    "rice": 6,
    "wheat": 4,
    "maize": 5,
    "millets": 3,
    "pulses": 3,
    "default": 4
}

@router.post("/recommend", response_model=ResponseModel)
def recommend_irrigation(payload: IrrigationRequest):
    crop = payload.crop.lower()
    crop_req = CROP_WATER_REQUIREMENT.get(crop, CROP_WATER_REQUIREMENT["default"])

    notes = []

    # Adjust based on season
    if payload.season.lower() == "kharif":
        notes.append("Kharif season: Higher rainfall expected, adjust irrigation accordingly.")
    elif payload.season.lower() == "rabi":
        notes.append("Rabi season: Cooler temperatures, lower evapotranspiration.")
    elif payload.season.lower() == "summer":
        notes.append("Summer season: High evapotranspiration, more frequent irrigation needed.")

    # Effective water availability
    effective_water = payload.soil_moisture + (payload.rainfall_mm / 10)  # crude estimate
    et = payload.evapotranspiration if payload.evapotranspiration > 0 else crop_req

    # Irrigation need
    irrigation_need = max(0, et * 7 - payload.rainfall_mm)  # for 1 week

    if payload.soil_moisture < 20:
        notes.append("Soil moisture is low (<20%). Immediate irrigation required.")
    elif 20 <= payload.soil_moisture < 40:
        notes.append("Soil moisture is moderate. Irrigation recommended within 2-3 days.")
    else:
        notes.append("Soil moisture is sufficient. Delay irrigation for now.")

    if payload.rainfall_mm < 10:
        notes.append("Low rainfall detected this week. Supplement with irrigation.")
    elif payload.rainfall_mm > 50:
        notes.append("Heavy rainfall received. Reduce irrigation to prevent waterlogging.")

    # Irrigation method suggestion
    if crop in ["rice"]:
        notes.append("Maintain standing water (2-5 cm) in rice fields for best yield.")
    elif crop in ["wheat", "maize", "millets", "pulses"]:
        notes.append("Adopt furrow or drip irrigation for efficient water use.")

    recommendations = {
        "weekly_irrigation_need_mm": irrigation_need,
        "daily_crop_requirement_mm": crop_req,
        "evapotranspiration_used_mm": et
    }

    return ResponseModel(
        success=True,
        data={
            "recommendations": recommendations,
            "notes": notes
        },
        message="Irrigation recommendation fetched successfully"
    )
