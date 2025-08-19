from fastapi import APIRouter
from app.models.pydantic_schemas import PriceRequest, PriceResponse
from app.services.market_service import fetch_market_price

router = APIRouter(prefix="/market", tags=["market-prices"])

@router.post("", response_model=PriceResponse)
def get_prices(req: PriceRequest):
    return fetch_market_price(req)
