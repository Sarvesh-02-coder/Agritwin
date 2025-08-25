from fastapi import APIRouter, HTTPException
from typing import Dict
from ..services import profile_service

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/")
def get_profiles():
    return {
        "success": True,
        "data": profile_service.get_profiles()
    }


@router.post("/")
def add_or_update(profile: Dict):
    if "phone" not in profile or not profile["phone"].strip():
        raise HTTPException(status_code=400, detail="Phone number is required")

    result = profile_service.add_or_update_profile(profile)

    # Differentiate between create, update, and no-change
    if result["message"] == "No changes detected":
        return {
            "success": False,
            "message": result["message"],
            "data": result["profile"]
        }
    elif result["message"] == "Profile updated successfully":
        return {
            "success": True,
            "message": result["message"],
            "data": result["profile"],
            "action": "updated"
        }
    else:  # Profile created
        return {
            "success": True,
            "message": result["message"],
            "data": result["profile"],
            "action": "created"
        }
