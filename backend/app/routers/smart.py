# # backend/app/routers/smart.py
# from fastapi import APIRouter, HTTPException
# from pathlib import Path

# from app.models.pydantic_schemas import Profile
# from app.schemas.response import ResponseModel
# from app.services.weather_service import fetch_weather_summary
# from app.services.advisors import (
#     recommend_crops,
#     irrigation_advice,
#     fertilizer_recommendation,
#     pest_alerts,
#     get_market_prices,
# )
# from app.services.soil_service import get

# router = APIRouter(prefix="/smart", tags=["Smart Advisor"])

# # Temporary in-memory store (TODO: replace with DB)
# PROFILES = {}

# DATA_DIR = Path(__file__).resolve().parents[3] / "ml" / "data"


# @router.post("/profile", response_model=ResponseModel)
# async def create_profile(profile: Profile):
#     """
#     Save a farmer profile in memory. 
#     (Future: integrate with persistent DB via profile_service).
#     """
#     PROFILES[profile.phone] = profile
#     return ResponseModel(
#         success=True,
#         data=profile.dict(),
#         message="✅ Profile saved successfully"
#     )


# @router.get("/{phone}", response_model=ResponseModel)
# async def smart_advice(phone: int):
#     """
#     Unified smart advisory pipeline. 
#     Uses farmer profile + weather + soil + ML advisors 
#     to generate actionable insights.
#     """
#     profile = PROFILES.get(phone)
#     if not profile:
#         raise HTTPException(status_code=404, detail="Profile not found")

#     # Validate profile has location
#     pincode = getattr(profile, "location", None)
#     if not pincode:
#         raise HTTPException(status_code=400, detail="Profile missing location")

#     try:
#         # --- 1) Weather summary ---
#         weather_summary = fetch_weather_summary(pincode)

#         # --- 2) Soil summary ---
#         soil = fetch_soil_summary(pincode)

#         # --- 3) Advisors ---
#         crops = recommend_crops(
#             soil_pH=soil.get("pH"),
#             rainfall_mm_7d=weather_summary.get("rainfall_7d_total"),
#             season="Kharif",  # TODO: auto-detect based on date/calendar
#         )

#         crop_choice = profile.crop or (crops[0]["crop"] if crops else "generic")

#         irrigation = irrigation_advice(
#             soil_moisture=soil.get("soil_moisture"),
#             rainfall_mm_7d=weather_summary.get("rainfall_7d_total"),
#             crop=crop_choice,
#         )

#         fert = fertilizer_recommendation(
#             n=soil.get("N"), p=soil.get("P"), k=soil.get("K"),
#             crop=crop_choice,
#             soil_pH=soil.get("pH"),
#         )

#         pests = pest_alerts(
#             crop=crop_choice,
#             temp_c=weather_summary.get("temp_7d_avg"),
#             humidity_pct=weather_summary.get("humidity_7d_avg"),
#             season="Kharif",
#         )

#         prices = get_market_prices(crop_choice)

#         result = {
#             "profile": profile.dict(),
#             "weather": weather_summary,
#             "soil": soil,
#             "recommendations": {
#                 "crops": crops,
#                 "irrigation": irrigation,
#                 "fertilizer": fert,
#                 "pests": pests,
#                 "market_prices": prices,
#             },
#         }

#         return ResponseModel(success=True, data=result, message="Smart advice generated successfully")

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Smart advisor failed: {str(e)}")
