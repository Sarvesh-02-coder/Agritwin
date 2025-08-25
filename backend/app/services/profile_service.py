import json
from pathlib import Path
from typing import Dict, List

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "profiles.json"
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_profiles() -> List[Dict]:
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_profiles(profiles: List[Dict]):
    with open(DATA_FILE, "w") as f:
        json.dump(profiles, f, indent=2)

def add_profile(profile: Dict) -> Dict:
    profiles = load_profiles()
    profiles.append(profile)
    save_profiles(profiles)
    return profile

def get_profiles() -> List[Dict]:
    return load_profiles()

def update_profile(phone: str, new_data: Dict) -> Dict:
    profiles = load_profiles()
    for p in profiles:
        if p["phone"] == phone:
            p.update(new_data)
            save_profiles(profiles)
            return p
    raise ValueError("Profile not found")
