import requests
from datetime import date, timedelta
from app.models.pydantic_schemas import PriceRequest, PriceResponse, PriceData

BASE_URL = "https://agmarknet.gov.in/api/Report/CommodityWiseDailyReport"

def fetch_market_price(req: PriceRequest) -> PriceResponse:
    today = date.today()
    start = (today - timedelta(days=7)).strftime("%d/%m/%Y")
    end = today.strftime("%d/%m/%Y")

    params = {
        "commodity": req.crop,
        "state": req.state,
        "district": req.district or "",
        "fromdate": start,
        "todate": end,
        "limit": 50
    }

    resp = requests.get(BASE_URL, params=params, timeout=30)
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
            prices.append(PriceData(mandi=mandi, date=date_str, price_per_quintal=price))
        except:
            continue

    avg_price = round(sum(all_prices) / len(all_prices), 2) if all_prices else 0

    return PriceResponse(
        crop=req.crop,
        state=req.state,
        district=req.district,
        avg_price=avg_price,
        prices=prices
    )
