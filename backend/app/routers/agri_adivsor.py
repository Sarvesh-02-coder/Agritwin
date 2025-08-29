# app/routers/agri_advisors.py

from fastapi import APIRouter, HTTPException
from app.services import recommend_service, pest_service, profile_service

router = APIRouter(prefix="/agri-advisor", tags=["Agri-Advisor"])


@router.get("/dashboard")
def get_dashboard():
    """
    Unified Agri-Advisor Dashboard:
    Returns exactly what frontend expects:
    {
      "profile": { ... },
      "recommendations": [ {crop, score, rationale}, ... ],
      "pest_alerts": [ {pest, disease, risk, note}, ... ]
    }
    """
    try:
        # ✅ Load active farmer profile
        profile = profile_service.get_active_profile()
        if not profile:
            raise HTTPException(status_code=404, detail="No active profile found")

        # ✅ Get crop recommendations (auto-uses profile/soil/weather)
        recommendations = recommend_service.get_recommendations()

        # ✅ Get pest/disease alerts (auto-uses profile/weather)
        pest_alerts = pest_service.get_pest_alerts()

        return {
            "profile": profile,
            "recommendations": recommendations,
            "pest_alerts": pest_alerts
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating dashboard data: {e}")
