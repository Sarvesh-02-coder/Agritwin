# app/routers/simulator.py
from fastapi import APIRouter, HTTPException
from app.models.pydantic_schemas import WhatIfRequest
from app.ml.inference import what_if_yield

router = APIRouter(prefix="/simulator", tags=["Simulator"])

@router.post("/simulate")
def simulate_endpoint(req: WhatIfRequest):
    """
    Accepts WhatIfRequest and returns a JSON object:
      {
        predicted_yield,
        growth_curve: [{week, yield}, ...],
        weather,
        soil,
        irrigation,
        input_overrides
      }
    """
    try:
        result = what_if_yield(req)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))