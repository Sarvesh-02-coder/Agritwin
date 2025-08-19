from fastapi import APIRouter
from app.models.pydantic_schemas import PestAlertRequest, PestAlertResponse
from app.services.pest_service import get_pest_alerts

router = APIRouter(prefix="/alerts/pests", tags=["pest-disease"])

@router.post("", response_model=PestAlertResponse)
def pest_alert(req: PestAlertRequest):
    alerts = get_pest_alerts(req)
    return PestAlertResponse(alerts=alerts)
