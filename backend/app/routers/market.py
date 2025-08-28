# backend/app/routers/market.py
from fastapi import APIRouter, HTTPException
from app.services.market_service import fetch_market_price
from app.schemas.response import ResponseModel

router = APIRouter(prefix="/market", tags=["Market Advisory"])


@router.get("/", response_model=ResponseModel)
async def fetch_market_prices():
    """
    Fetch market prices for the crop in the active profile.
    Uses AgMarkNet API (via market_service) with fallback to mock prices.
    """
    try:
        prices = fetch_market_price()  # ✅ profile-driven, no params needed

        if not prices:
            raise HTTPException(status_code=404, detail="No market price data available")

        return ResponseModel(
            success=True,
            data=prices.dict(),  # ✅ Pydantic → dict
            message=(
                f"Market prices for {prices.crop} "
                f"in {prices.state}{' - ' + prices.district if prices.district else ''} fetched successfully"
            ),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
