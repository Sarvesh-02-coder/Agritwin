from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.schemas.response import ResponseModel, CropRecommendationItem, CropData

router = APIRouter(
    prefix="/crop",
    tags=["Crop Recommendation"]
)

# Input schema for crop recommendations
class CropInput(BaseModel):
    soil_pH: float
    rainfall_mm: float
    season: str  # e.g., "kharif", "rabi", "summer"
    soil_moisture: float


@router.post("/recommend", response_model=ResponseModel)
async def recommend_crop(input: CropInput):
    """
    Return structured crop recommendations and notes (list).
    Uses only the shared schema file (app.schemas.response).
    """
    recommendations: List[CropRecommendationItem] = []
    notes: List[str] = []

    # --- Crop suggestion rules (simple, extendable) ---
    s_pH = input.soil_pH
    rain = input.rainfall_mm
    season = input.season.lower()
    moisture = input.soil_moisture

    # Rice candidate
    if 5.5 <= s_pH <= 7.0 and rain >= 800 and season == "kharif":
        recommendations.append(CropRecommendationItem(crop="rice", reason="Neutral pH and adequate rainfall in Kharif."))

    # Maize candidate
    if 5.5 <= s_pH <= 7.5 and rain >= 500:
        recommendations.append(CropRecommendationItem(crop="maize", reason="Wide pH tolerance and moderate rainfall."))

    # Millets for low moisture
    if moisture < 25:
        recommendations.append(CropRecommendationItem(crop="millets", reason="Tolerates low soil moisture and drought conditions."))

    # Wheat in rabi if conditions OK
    if season == "rabi" and 6.0 <= s_pH <= 7.5 and 400 <= rain <= 800:
        recommendations.append(CropRecommendationItem(crop="wheat", reason="Favorable pH and moderate water requirement in Rabi season."))

    # Pulses fallback for summer/low rainfall
    if season == "summer" and rain < 400:
        recommendations.append(CropRecommendationItem(crop="pulses", reason="Thrives in low rainfall and warm summer conditions."))

    # --- Notes (always list) ---
    if s_pH < 6.0:
        notes.append("Soil is slightly acidic. Lime application recommended to raise pH.")
    elif s_pH > 7.5:
        notes.append("Soil is alkaline. Consider gypsum, sulfur, or organic amendments to balance pH.")
    else:
        notes.append("Soil pH is within the optimal range for most crops.")

    if rain < 400:
        notes.append("Rainfall is low. Consider drought-tolerant crops and efficient irrigation (drip/mulching).")
    elif rain > 1200:
        notes.append("Rainfall is high. Ensure proper drainage and choose flood-tolerant varieties where needed.")
    else:
        notes.append("Rainfall is moderate.")

    if moisture < 25:
        notes.append("Soil moisture is low. Use mulching and water-conservation techniques.")
    elif moisture > 60:
        notes.append("Soil moisture is high. Ensure good drainage to prevent root diseases.")
    else:
        notes.append("Soil moisture is within a good range.")

    # --- Fallback if no specific crops chosen ---
    if not recommendations:
        recommendations.append(CropRecommendationItem(crop="pulses", reason="Suitable under a wide range of soil and rainfall conditions."))

    # Build response data using shared types in app.schemas.response
    crop_data = CropData(recommendations=recommendations, notes=notes)

    return ResponseModel(
        success=True,
        data=crop_data,
        message="Crop recommendation fetched successfully"
    )
