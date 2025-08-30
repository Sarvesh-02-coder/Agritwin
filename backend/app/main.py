from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

load_dotenv()
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
from app.routers.simulator import router as simulator

# Translator
from app.services.translator_service import translate_text

app = FastAPI(title="AgriTwin Backend", version="0.1.0")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Translation Middleware ---
@app.middleware("http")
async def translation_middleware(request: Request, call_next):
    lang = request.query_params.get("lang", "en")  # ?lang=hi or ?lang=mr
    response = await call_next(request)

    if isinstance(response, JSONResponse) and isinstance(response.body, (bytes, bytearray)):
        import json
        try:
            body = json.loads(response.body.decode())

            def translate_obj(obj):
                if isinstance(obj, dict):
                    return {k: translate_obj(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [translate_obj(v) for v in obj]
                elif isinstance(obj, str):
                    return translate_text(obj, lang)
                return obj

            translated = translate_obj(body)
            return JSONResponse(content=translated, status_code=response.status_code)

        except Exception as e:
            print(f"[Middleware Translation Error]: {e}")
            return response

    return response

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
app.include_router(simulator)

# -------------------------
# Serve Frontend (dist/)
# -------------------------
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")

if os.path.isdir(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

    # fallback: serve index.html for React/Vue/SPA routes
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        index_file = os.path.join(frontend_path, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"error": "Frontend not found"}
