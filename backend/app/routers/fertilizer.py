# backend/app/routers/fertilizer.py
from fastapi import APIRouter, HTTPException
from app.models.pydantic_schemas import FertilizerRequest
from app.schemas.response import ResponseModel
from app.services import advisors

router = APIRouter(
    prefix="/fertilizer",
    tags=["Fertilizer Recommendation"]
)

@router.post("/recommend", response_model=ResponseModel)
def recommend_fertilizer(payload: FertilizerRequest):
    """
    Get fertilizer recommendations based on crop NPK requirements and soil pH.
    """
    try:
        recommendations = advisors.fertilizer_recommendation(
            n=payload.n,
            p=payload.p,
            k=payload.k,
            crop=payload.crop,
            soil_pH=payload.soil_pH,
        )

        return ResponseModel(
            success=True,
            data=recommendations,
            message="Fertilizer recommendation fetched successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
