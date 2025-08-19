import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

# Save location
DATA_PATH = Path(__file__).resolve().parents[0] / "data" / "soil_health_card.csv"

BASE_URL = "https://soilhealth.dac.gov.in/"

def fetch_soil_data(pincode: str):
    """
    Prototype: fetch soil health data from SHC portal for a given pincode.
    """
    # NOTE: This endpoint is only a placeholder! The SHC site uses ASP.NET forms,
    # so we might need to inspect their API calls. For now, let's try a GET request.
    url = f"{BASE_URL}SoilCard/soilhealthcard?pincode={pincode}"

    resp = requests.get(url, timeout=20)
    if resp.status_code != 200:
        print(f"❌ Failed to fetch data for {pincode}")
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # Example scraping logic (this will depend on how SHC shows data)
    rows = soup.find_all("tr")
    soil_data = {"pincode": pincode}

    for row in rows:
        cols = [c.text.strip() for c in row.find_all("td")]
        if len(cols) == 2:
            key, value = cols
            soil_data[key.lower().replace(" ", "_")] = value

    return soil_data


if __name__ == "__main__":
    pincode = input("Enter pincode: ").strip()
    data = fetch_soil_data(pincode)

    if data:
        df = pd.DataFrame([data])
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

        if DATA_PATH.exists():
            df.to_csv(DATA_PATH, mode="a", header=False, index=False)
        else:
            df.to_csv(DATA_PATH, index=False)

        print(f"✅ Saved soil data for {pincode} to {DATA_PATH}")
    else:
        print("⚠️ No data found")
