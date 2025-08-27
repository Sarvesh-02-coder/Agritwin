# app/routers/soil.py

from fastapi import APIRouter, HTTPException
from app.services.soil_service import summarize_soil
import traceback

router = APIRouter(prefix="/soil", tags=["Soil"])


@router.get("/{pincode}")
def get_soil(pincode: str):
    """
    Fetch soil data summary for a given pincode.
    Example: GET /soil/110001
    """
    try:
        data = summarize_soil(pincode)  # ✅ synchronous
        if not data:
            raise HTTPException(
                status_code=404,
                detail=f"No soil data found for pincode {pincode}. Likely an urban/city area."
            )
        return {
            "success": True,
            "pincode": pincode,
            "soil_data": data
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        print("❌ Soil API error:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error - check backend logs")
