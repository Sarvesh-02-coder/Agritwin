from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict

# ---------- Crop Recommendation ----------
class CropRecommendRequest(BaseModel):
    season: str
    soil_pH: float
    rainfall_mm: float
    region: Optional[str] = None

class CropRecommendation(BaseModel):
    crop: str
    score: float
    rationale: str

class CropRecommendResponse(BaseModel):
    recommendations: List[CropRecommendation]


# ---------- Irrigation ----------
class IrrigationRequest(BaseModel):
    crop: str
    area_hectares: float
    soil_moisture: float  # % volumetric water content
    pincode: str          # Needed to fetch NASA weather

class IrrigationProfile(BaseModel):
    crop: str
    farmArea: float
    location: str   # pincode

class IrrigationResponse(BaseModel):
    water_needed_mm: float
    water_needed_liters: float
    rationale: str
    weather_summary: dict
    weather_weekly: List[dict]


# ---------- Fertilizer ----------
SoilLevel = Literal["low", "medium", "high"]

class FertilizerRequest(BaseModel):
    crop: str = Field(..., description="Crop name, e.g., rice, wheat, maize")
    area_ha: float = Field(..., gt=0, description="Farm area in hectares")
    season: Optional[str] = Field(None, description="kharif/rabi/annual (optional)")
    soil_pH: Optional[float] = Field(None, description="Soil pH if known")
    soil_N_level: SoilLevel = "medium"
    soil_P_level: SoilLevel = "medium"
    soil_K_level: SoilLevel = "medium"
    yield_target: Optional[float] = Field(
        None, description="Optional target yield (t/ha) to bias N slightly"
    )

class FertilizerDose(BaseModel):
    name: str
    per_ha_kg: float
    total_kg: float
    contributes: Dict[str, float]  # e.g. {"N": 46.0}

class FertilizerAdvice(BaseModel):
    per_ha_NPK_kg: Dict[str, float]    # {"N": 100, "P2O5": 60, "K2O": 40}
    total_NPK_kg: Dict[str, float]
    fertilizer_plan: List[FertilizerDose]
    application_schedule: List[str]
    cautions: List[str]
    rationale: List[str]


# ---------- Pest ----------
class PestAlertRequest(BaseModel):
    crop: str
    season: Optional[str] = None
    temp_c: Optional[float] = None
    humidity_pct: Optional[float] = None
    pincode: Optional[str] = None   # ✅ restored for backward compatibility

class PestDiseaseAlert(BaseModel):
    pest: str
    disease: str
    risk: str
    note: Optional[str] = None

class PestAlertResponse(BaseModel):
    alerts: List[PestDiseaseAlert]


# ---------- Price ----------
class PriceRequest(BaseModel):
    crop: str
    state: str
    district: Optional[str] = None

class PriceData(BaseModel):
    mandi: str
    date: str
    price_per_quintal: float

class PriceResponse(BaseModel):
    crop: str
    state: Optional[str] = None
    district: Optional[str] = None
    avg_price: float
    prices: List[PriceData]


# ---------- Farm Report ----------
class FarmReportRequest(BaseModel):
    soil_pH: Optional[float] = None
    rainfall_mm_7d: Optional[float] = None
    season: Optional[str] = None
    soil_moisture: Optional[float] = None
    n: Optional[float] = None
    p: Optional[float] = None
    k: Optional[float] = None
    crop: Optional[str] = None
    temp_c: Optional[float] = None
    humidity_pct: Optional[float] = None


# ---------- Market ----------
class MarketRequest(BaseModel):
    commodity: str
    state: Optional[str] = None
    district: Optional[str] = None


# ---------- Pest Request ----------
class PestRequest(BaseModel):
    crop: str
    season: Optional[str] = None
    temp_c: Optional[float] = None
    humidity_pct: Optional[float] = None


# ---------- Profile ----------
class Profile(BaseModel):
    name: str
    phone: str
    location: str
    crop: Optional[str] = None
    smsAlerts: bool = False
    farmArea: float


# ---------- Risk Forecast ----------
class YieldIncomePoint(BaseModel):
    month: str
    yield_pct: float
    income_inr: float

class RiskFactor(BaseModel):
    factor: str
    risk_pct: float

class RiskForecastResponse(BaseModel):
    expected_yield_pct: float
    expected_income_inr: float
    harvest_date: str
    overall_risk_level: str  # Low / Medium / High
    overall_risk_score: float

    yield_forecast: List[YieldIncomePoint]
    risk_factors: List[RiskFactor]
    note: str


# ---------- What-If Simulator ----------
class WhatIfRequest(BaseModel):
    crop: Optional[str] = None
    pincode: Optional[str] = None
    area_ha: Optional[float] = None
    season: Optional[str] = None

    # Overrides
    rainfall_mm: Optional[float] = None
    temp_c: Optional[float] = None
    humidity_pct: Optional[float] = None
    soil_pH: Optional[float] = None

    # New inputs from frontend
    sowing_delay: Optional[int] = 0        # delay in weeks
    irrigation_delay: Optional[int] = 0    # delay in weeks
