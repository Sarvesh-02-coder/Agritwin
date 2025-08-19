from fastapi import APIRouter
from app.models.pydantic_schemas import CropRecommendRequest, CropRecommendResponse
from app.services.crop_service import recommend_crops

router = APIRouter(prefix="/recommend/crops", tags=["crop-recommendation"])

@router.post("", response_model=CropRecommendResponse)
def recommend(req: CropRecommendRequest):
    recs = recommend_crops(req)
    return CropRecommendResponse(recommendations=recs)
