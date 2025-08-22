from fastapi import APIRouter, HTTPException
from app.services.weather_service import fetch_weather

router = APIRouter(prefix="/weather", tags=["Weather Service"])

@router.get("/{pincode}")
def get_weather(pincode: str, days: int = 30):
    """
    Fetch weather data for a given pincode and return CSV path.
    """
    try:
        csv_path = fetch_weather(pincode, days)
        return {"message": f"✅ Weather data saved", "csv_path": str(csv_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
