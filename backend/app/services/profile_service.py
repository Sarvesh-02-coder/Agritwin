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
    # If this is the first profile, make it active
    if not profiles:
        profile["active"] = True
    else:
        profile["active"] = False

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


# 🔹 New function: Switch active profile
def switch_profile(phone: str) -> Dict:
    profiles = load_profiles()
    phone = phone.strip()
    found = None

    for p in profiles:
        if p["phone"] == phone:
            found = p

    if not found:
        return {"message": "Profile not found", "profile": None}

    # Clear all active flags
    for p in profiles:
        p["active"] = False

    # Set this one active
    found["active"] = True
    save_profiles(profiles)

    return {"message": "Profile switched successfully", "profile": found}


# 🔹 Helper: get the active profile
def get_active_profile() -> Optional[Dict]:
    profiles = load_profiles()
    for p in profiles:
        if p.get("active"):
            return p
    return None
