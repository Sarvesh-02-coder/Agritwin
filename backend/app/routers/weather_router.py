# app/routers/weather.py
from fastapi import APIRouter, HTTPException, Query
from app.services import weather_service
from app.schemas.response import ResponseModel

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/fetch", response_model=ResponseModel)
def fetch_weather_data(pincode: str = Query(..., description="Indian postal code")):
    """
    Fetch last 30 days weather data for given pincode.
    Saves CSV and returns file path.
    """
    try:
        csv_path = weather_services.fetch_weather(pincode, days=30)
        return ResponseModel.success(
            message=f"Weather data fetched for pincode {pincode}",
            data={"csv_path": str(csv_path)}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary", response_model=ResponseModel)
def get_weather_summary(pincode: str = Query(..., description="Indian postal code")):
    """
    Get summarized weather insights for last 7 days.
    Returns JSON with rainfall, avg temperature, avg humidity.
    """
    try:
        summary = weather_services.fetch_weather_summary(pincode)
        return ResponseModel.success(
            message=f"7-day weather summary for pincode {pincode}",
            data=summary
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
