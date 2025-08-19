from fastapi import APIRouter
from app.models.pydantic_schemas import IrrigationRequest, IrrigationResponse
from app.services.irrigation_service import calculate_irrigation

router = APIRouter(prefix="/advisory/irrigation", tags=["irrigation"])

@router.post("", response_model=IrrigationResponse)
def irrigation_advice(req: IrrigationRequest):
    return calculate_irrigation(req)
