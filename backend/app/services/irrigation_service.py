from app.models.pydantic_schemas import IrrigationRequest, IrrigationResponse

# Approx crop water requirement (mm/week)
CROP_WATER_REQ = {
    "rice": 50,
    "wheat": 30,
    "maize": 35,
    "sugarcane": 60,
    "cotton": 40,
    "pulses": 25,
    "millets": 20
}

def calculate_irrigation(req: IrrigationRequest) -> IrrigationResponse:
    base_need = CROP_WATER_REQ.get(req.crop.lower(), 30)  # default = 30 mm/week
    
    # Adjust for soil moisture
    if req.soil_moisture > 30:   # already moist
        base_need *= 0.7
    elif req.soil_moisture < 15: # very dry
        base_need *= 1.3

    # Adjust for rainfall forecast
    water_deficit = base_need - req.rainfall_forecast_mm
    water_deficit = max(water_deficit, 0)

    # Convert mm to liters (1 mm = 10,000 L/hectare)
    liters = water_deficit * req.area_hectares * 10000

    return IrrigationResponse(
        water_needed_mm=round(water_deficit, 2),
        water_needed_liters=round(liters, 2),
        rationale=f"{req.crop} requires ~{base_need} mm/week. Rainfall forecast reduces net need."
    )
