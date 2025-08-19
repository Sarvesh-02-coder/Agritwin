from fastapi import APIRouter
from app.models.pydantic_schemas import FertilizerRequest, FertilizerAdvice
from app.services.fertilizer_service import get_fertilizer_advice

router = APIRouter(prefix="/advice/fertilizer", tags=["fertilizer"])

@router.post("", response_model=FertilizerAdvice)
def advise(req: FertilizerRequest):
    return get_fertilizer_advice(req)
