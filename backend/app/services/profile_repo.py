from pathlib import Path
import json
from typing import Optional, Dict, Any

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
PROFILES_FILE = DATA_DIR / "profiles.json"

def load_profiles() -> Dict[str, Any]:
    if not PROFILES_FILE.exists():
        return {"profiles": []}
    with open(PROFILES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_profile(phone: str) -> Optional[dict]:
    data = load_profiles()
    for p in (data if isinstance(data, list) else data.get("profiles", [])):
        if p.get("phone") == phone:
            return p
    return None
