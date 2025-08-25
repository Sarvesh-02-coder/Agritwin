import json
from pathlib import Path
from typing import Dict, List, Optional

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "profiles.json"
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_profiles() -> List[Dict]:
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_profiles(profiles: List[Dict]):
    with open(DATA_FILE, "w") as f:
        json.dump(profiles, f, indent=2)


def add_or_update_profile(profile: Dict) -> Dict:
    profiles = load_profiles()
    phone = profile["phone"].strip()

    for idx, p in enumerate(profiles):
        if p["phone"] == phone:
            # If exactly same, do nothing
            if p == profile:
                return {"message": "No changes detected", "profile": p}

            # Update existing
            profiles[idx] = profile
            save_profiles(profiles)
            return {"message": "Profile updated successfully", "profile": profile}

    # New profile
    profiles.append(profile)
    save_profiles(profiles)
    return {"message": "Profile created successfully", "profile": profile}


def get_profiles() -> List[Dict]:
    return load_profiles()


def get_profile_by_phone(phone: str) -> Optional[Dict]:
    profiles = load_profiles()
    for p in profiles:
        if p["phone"] == phone.strip():
            return p
    return None
