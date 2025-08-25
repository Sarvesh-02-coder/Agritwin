from fastapi import APIRouter
from pydantic import BaseModel
from app.schemas.response import ResponseModel  # ✅ Correct import

router = APIRouter(
    prefix="/pest",
    tags=["Pest & Disease Management"]
)

# Input schema
class PestRequest(BaseModel):
    crop: str
    season: str
    avg_temp_c: float       # average temperature °C
    avg_humidity: float     # average relative humidity %
    recent_rainfall_mm: float

# Knowledge base: major pest/disease conditions
PEST_DISEASE_DB = {
    "rice": [
        {
            "name": "Rice Blast",
            "condition": lambda t, h, r: 20 <= t <= 28 and h > 80 and r > 50,
            "advice": "Fungal disease. Use resistant varieties, avoid excessive nitrogen, apply Tricyclazole if severe."
        },
        {
            "name": "Brown Planthopper",
            "condition": lambda t, h, r: t > 28 and h > 70,
            "advice": "Pest attack. Maintain proper spacing, avoid overuse of urea, use neem-based spray if needed."
        }
    ],
    "wheat": [
        {
            "name": "Rust (Yellow/Stem/Leaf)",
            "condition": lambda t, h, r: 10 <= t <= 25 and h > 60,
            "advice": "Fungal rust common in cool humid conditions. Use resistant cultivars, apply Propiconazole if outbreak detected."
        }
    ],
    "maize": [
        {
            "name": "Fall Armyworm",
            "condition": lambda t, h, r: t > 20,
            "advice": "Larvae damage leaves and cobs. Regular scouting, pheromone traps, and biocontrol (Trichogramma) recommended."
        }
    ],
    "pulses": [
        {
            "name": "Pod Borer",
            "condition": lambda t, h, r: t > 20 and h > 60,
            "advice": "Install pheromone traps, encourage natural enemies, avoid indiscriminate insecticide sprays."
        }
    ],
    "millets": [
        {
            "name": "Shoot Fly",
            "condition": lambda t, h, r: t > 25,
            "advice": "Use timely sowing, resistant varieties, and seed treatment with Imidacloprid for prevention."
        }
    ]
}

@router.post("/recommend", response_model=ResponseModel)
def recommend_pest_management(payload: PestRequest):
    crop = payload.crop.lower()
    possible_threats = []
    notes = []

    if crop in PEST_DISEASE_DB:
        for issue in PEST_DISEASE_DB[crop]:
            if issue["condition"](payload.avg_temp_c, payload.avg_humidity, payload.recent_rainfall_mm):
                possible_threats.append({
                    "name": issue["name"],
                    "advice": issue["advice"]
                })

    if not possible_threats:
        notes.append("No major pest or disease risk detected based on current conditions.")
    else:
        notes.append("Conditions favorable for certain pest/disease occurrence. Monitor crop regularly.")

    # General IPM (Integrated Pest Management) notes
    notes.extend([
        "Adopt crop rotation and field sanitation to reduce pest cycles.",
        "Encourage natural predators (ladybird beetles, spiders, wasps).",
        "Use chemical pesticides only as a last resort, following recommended doses."
    ])

    return ResponseModel(
        success=True,
        data={
            "crop": crop,
            "possible_threats": possible_threats,
            "notes": notes
        },
        message="Pest & disease management recommendation fetched successfully"
    )
