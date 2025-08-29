from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.routers.crop import router as crop_router
from app.routers.irrigation import router as irrigation_router
from app.routers.fertilizer import router as fertilizer_router
from app.routers.pest import router as pest_router
from app.routers.market import router as market_router
from app.routers.weather_router import router as weather_router
from app.routers.farm_report import router as farm_report_router
from app.routers.profile_router import router as profile_router
from app.routers.forecast import router as forecast_router
# from app.routers.smart import router as smart_router
from app.routers.soil import router as soil_router
from app.routers import dashboard
from app.chatbot.backend.app import router as chatbot_router
from app.routers.agri_adivsor import router as pest


app = FastAPI(title="AgriTwin Backend", version="0.1.0")

# --- CORS (lock down origins in prod) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # e.g. ["http://localhost:3000"] in dev, your domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Health check ---
@app.get("/health")
def health():
    return {"status": "ok", "service": "AgriTwin Backend"}

# --- Routers ---
app.include_router(crop_router)
app.include_router(irrigation_router)
app.include_router(fertilizer_router)
app.include_router(pest_router)
app.include_router(market_router)
app.include_router(weather_router)
app.include_router(farm_report_router)
app.include_router(profile_router)
# app.include_router(smart_router)
app.include_router(dashboard.router)
app.include_router(soil_router)
app.include_router(forecast_router)
app.include_router(chatbot_router)
app.include_router(pest)

