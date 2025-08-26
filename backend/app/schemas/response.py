from typing import Any, Dict, List, Optional
from pydantic import BaseModel

# Generic wrapper used by most endpoints
class ResponseModel(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: str

# Fertilizer-specific schema (keeps notes as list)
class FertilizerRecommendation(BaseModel):
    N_required_kg_ha: float
    P_required_kg_ha: float
    K_required_kg_ha: float
    notes: List[str]

class FertilizerData(BaseModel):
    recommendations: FertilizerRecommendation

class FertilizerResponse(BaseModel):
    success: bool
    data: FertilizerData
    message: str

# Crop-specific schema
class CropRecommendationItem(BaseModel):
    crop: str
    reason: str

class CropData(BaseModel):
    recommendations: List[CropRecommendationItem]
    notes: List[str]

class CropResponse(BaseModel):
    success: bool
    data: CropData
    message: str

class FarmReportResponse(BaseModel):
    crop_recommendations: Optional[List[Dict[str, Any]]] = None
    irrigation: Optional[Dict[str, Any]] = None
    fertilizer: Optional[Dict[str, Any]] = None
    pest_alerts: Optional[List[Dict[str, Any]]] = None
    market: Optional[Dict[str, Any]] = None

class MarketResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: str

from typing import Optional, Any, List
from pydantic import BaseModel

class ProfileResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: str

class PestResponse(BaseModel):
    success: bool
    data: Optional[List[str]] = None
    message: str

class APIResponse(BaseModel):
    """
    Standardized API response wrapper
    """
    status: str = "success"
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """
    Error response format
    """
    status: str = "error"
    message: str
    details: Optional[Dict[str, Any]] = None


# --- Specialized Responses for Irrigation ---
class WeeklyWeatherData(BaseModel):
    date: str
    temperature_C: float
    humidity_pct: float
    rainfall_mm: float
    sunlight_hours: float


class IrrigationAdviceResponse(BaseModel):
    water_needed_mm: float
    water_needed_liters: float
    rationale: str
    weather_summary: Dict[str, float]
    weather_weekly: List[WeeklyWeatherData]