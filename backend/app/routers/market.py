# backend/app/routers/market.py
from fastapi import APIRouter, HTTPException, Query
from app.services.advisors import get_market_prices
from app.schemas.response import ResponseModel

router = APIRouter(prefix="/market", tags=["Market Advisory"])


@router.get("/", response_model=ResponseModel)
async def fetch_market_prices(
    crop: str = Query(..., description="Crop name (e.g., wheat, rice, maize)"),
    state: str = Query(..., description="Indian state"),
    district: str = Query(None, description="Optional district")
):
    """
    Fetch market prices for a given crop in a particular state/district.
    Uses AgMarkNet / internal advisory service.
    """
    try:
        prices = get_market_prices(crop=crop, state=state, district=district)

        if not prices:
            raise HTTPException(status_code=404, detail="No market price data available")

        return ResponseModel(
            success=True,
            data=prices,
            message=f"Market prices for {crop} in {state}{' - ' + district if district else ''} fetched successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
