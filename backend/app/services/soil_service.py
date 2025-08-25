import sys
import pandas as pd
from pathlib import Path

# Add project root (2 levels up from services/) to sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.ml.fetch_soil_shc import fetch_soil_data
  # reuse your existing scraper

# Path to where soil health data CSV will be saved
DATA_PATH = Path(__file__).resolve().parents[3] / "ml" / "data" / "soil_health_card.csv"


def fetch_soil_summary(pincode: str) -> dict:
    """
    Get soil summary for a given pincode.
    1. Try fetching fresh data from SHC portal.
    2. If failed, fallback to cached CSV data.
    """

    data = fetch_soil_data(pincode)

    if data:
        # Save new record into CSV
        df = pd.DataFrame([data])
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

        if DATA_PATH.exists():
            df.to_csv(DATA_PATH, mode="a", header=False, index=False)
        else:
            df.to_csv(DATA_PATH, index=False)

        print(f"✅ Soil data fetched and saved for {pincode}")
    else:
        print(f"⚠️ No fresh soil data for {pincode}, checking CSV...")
        if DATA_PATH.exists():
            df = pd.read_csv(DATA_PATH)
            row = df[df["pincode"].astype(str) == str(pincode)]
            if not row.empty:
                data = row.iloc[-1].to_dict()
            else:
                data = {}
        else:
            data = {}

    # Prepare summary with sensible defaults
    return {
        "pH": float(data.get("ph", 6.8)) if data else 6.8,
        "N": float(data.get("nitrogen", 0)) if data else None,
        "P": float(data.get("phosphorus", 0)) if data else None,
        "K": float(data.get("potassium", 0)) if data else None,
        "soil_moisture": 25.0  # Placeholder until real sensor integration
    }
