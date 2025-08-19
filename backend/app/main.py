from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from app.services.weather_service import fetch_weather as get_weather
from app.ml.inference import predict_yield
from app.routers.crop import router as crop_router
from app.routers.irrigation import router as irrigation_router
from app.routers.fertilizer import router as fertilizer_router
from app.routers.pest import router as pest_router
from app.routers import market
app = FastAPI(title="AgriTwin Backend", version="0.1.0")
app = FastAPI(title="AgriTwin API")
app.include_router(crop_router)
app.include_router(irrigation_router)  
app.include_router(fertilizer_router)
app.include_router(pest_router)
app.include_router(market.router)


# ---------------- Health Check ----------------
@app.get("/")
def health():
    return {"status": "ok", "service": "AgriTwin Backend"}


# ---------------- Weather Endpoint ----------------
from pydantic import BaseModel

class WeatherRequest(BaseModel):
    lat: float
    lon: float
    days: int = 7

@app.post("/weather")
def weather(req: WeatherRequest):
    """
    Fetch weather data from NASA POWER API
    """
    try:
        data = get_weather(req.lat, req.lon, req.days)
        return {
            "lat": req.lat,
            "lon": req.lon,
            "days": req.days,
            "message": "Weather data fetched successfully",
            "sample_keys": list(data.keys())
        }
    except Exception as e:
        return {"error": str(e)}



# ---------------- Yield Prediction ----------------
class YieldInput(BaseModel):
    soil_moisture_: float  # %
    soil_pH: float
    temperature_C: float
    rainfall_mm: float
    humidity_: float
    sunlight_hours: float
    crop_type: str
    irrigation_type: str
    fertilizer_type: str
    NDVI_index: float
    total_days: int
    pesticide_usage_ml: Optional[float] = 0.0

    class Config:
        json_schema_extra = {
            "example": {
                "soil_moisture_": 22,
                "soil_pH": 6.5,
                "temperature_C": 28,
                "rainfall_mm": 150,
                "humidity_": 70,
                "sunlight_hours": 8,
                "crop_type": "rice",
                "irrigation_type": "drip",
                "fertilizer_type": "urea",
                "NDVI_index": 0.72,
                "total_days": 120,
                "pesticide_usage_ml": 15.5
            }
        }


@app.post("/predict/yield")
def yield_prediction(input_data: YieldInput):
    """
    Predict yield (kg/hectare) based on soil, weather, and crop data.
    """
    try:
        result = predict_yield(input_data.dict())
        return {"predicted_yield_kg_per_hectare": result}
    except Exception as e:
        return {"error": str(e)}
