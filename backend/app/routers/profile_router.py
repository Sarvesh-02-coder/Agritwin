# backend/app/routers/profile_router.py
from fastapi import APIRouter, HTTPException
from app.models.pydantic_schemas import Profile
from app.services import profile_service
from app.schemas.response import ProfileResponse

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.post("/", response_model=ProfileResponse)
def create_profile(profile: Profile):
    """
    Create a new user profile.
    """
    try:
        created = profile_service.add_profile(profile.dict())
        return ProfileResponse(success=True, data=created, message="Profile created successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=ProfileResponse)
def read_profiles():
    """
    Fetch all profiles.
    """
    try:
        profiles = profile_service.get_profiles()
        return ProfileResponse(success=True, data=profiles, message="Profiles fetched successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{phone}", response_model=ProfileResponse)
def update_profile(phone: str, profile: Profile):
    """
    Update an existing profile by phone number.
    """
    try:
        updated = profile_service.update_profile(phone, profile.dict())
        return ProfileResponse(success=True, data=updated, message="Profile updated successfully")
    except ValueError:
        raise HTTPException(status_code=404, detail="Profile not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
