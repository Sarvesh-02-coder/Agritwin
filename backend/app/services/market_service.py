# app/services/market_service.py
import requests
import random
from datetime import date, timedelta
from app.models.pydantic_schemas import PriceResponse, PriceData
from app.services import profile_service

BASE_URL = "https://agmarknet.gov.in/api/Report/CommodityWiseDailyReport"
GEOCODE_URL = "https://nominatim.openstreetmap.org/search"


def pincode_to_state_district(pincode: str):
    """Convert pincode → (state, district) using OpenStreetMap Nominatim."""
    try:
        resp = requests.get(
            GEOCODE_URL,
            params={"q": pincode, "format": "json", "addressdetails": 1, "limit": 1},
            headers={"User-Agent": "AgriTwin/1.0"},
            timeout=10,
        )
        resp.raise_for_status()
        results = resp.json()
        if results:
            addr = results[0].get("address", {})
            state = addr.get("state")
            district = (
                addr.get("county")
                or addr.get("state_district")
                or addr.get("region")
                or ""
            )
            return state, district
    except Exception:
        pass
    return None, None


def fetch_market_price() -> PriceResponse:
    """
    Fetch mandi market prices for the active profile's crop, state, and district.
    Falls back to mock/static data if API fails (MVP safe).
    """
    # 🔹 Load active profile
    profile = profile_service.get_active_profile()
    if not profile:
        raise ValueError("No active profile found")

    crop = profile.get("crop")
    pincode = profile.get("location")  # profile stores pincode in `location`

    # 🔹 Convert pincode → state & district
    state, district = pincode_to_state_district(pincode)
    if not state:
        state = ""
    if not district:
        district = ""

    today = date.today()
    start = (today - timedelta(days=7)).strftime("%d/%m/%Y")
    end = today.strftime("%d/%m/%Y")

    params = {
        "commodity": crop,
        "state": state,
        "district": district,
        "fromdate": start,
        "todate": end,
        "limit": 50,
    }

    try:
        resp = requests.get(BASE_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        prices = []
        all_prices = []
        for entry in data.get("records", []):
            mandi = entry.get("Market", "Unknown")
            price = entry.get("Modal_Price", 0)
            date_str = entry.get("Arrival_Date", "")
            try:
                price = float(price)
                all_prices.append(price)
                prices.append(
                    PriceData(mandi=mandi, date=date_str, price_per_quintal=price)
                )
            except:
                continue

        if all_prices:
            avg_price = round(sum(all_prices) / len(all_prices), 2)
            return PriceResponse(
                crop=crop,
                state=state,
                district=district,
                avg_price=avg_price,
                prices=prices,
            )

    except Exception:
        # 🔹 Fallback to mock prices
        pass

    # -------- MOCK PRICES (MVP) --------
    base_prices = {
        "rice": 2200, "wheat": 2100, "maize": 1800,
        "cotton": 6000, "sugarcane": 300, "pulses": 5000, "millets": 2000
    }
    avg_price = base_prices.get(crop.lower(), 2000) + random.randint(-200, 200)

    mock_prices = [
        PriceData(mandi="Mock Mandi", date=str(today), price_per_quintal=avg_price)
    ]

    return PriceResponse(
        crop=crop,
        state=state,
        district=district,
        avg_price=avg_price,
        prices=mock_prices,
    )
