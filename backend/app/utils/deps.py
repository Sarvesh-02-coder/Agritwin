from fastapi import HTTPException, Query
from app.services.profile_repo import get_profile

def require_profile(phone: str = Query(..., description="Farmer phone in profile store")) -> dict:
    prof = get_profile(phone)
    if not prof:
        raise HTTPException(status_code=404, detail=f"Profile not found for {phone}")
    return prof
