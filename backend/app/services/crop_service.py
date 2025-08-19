from typing import List
from app.models.pydantic_schemas import CropRecommendRequest, CropRecommendation

# simple rules (you can expand later)
CROP_RULES = [
    # crop, (pH_min, pH_max), (rain_min, rain_max), seasons, note
    ("rice", (5.5, 7.0), (800, 2000), {"kharif"}, "Thrives in high rainfall & neutral pH"),
    ("wheat", (6.0, 7.5), (300, 900), {"rabi"}, "Prefers cooler season & moderate rain"),
    ("maize", (5.5, 7.5), (500, 1200), {"kharif", "rabi"}, "Wide pH tolerance; moderate rain"),
    ("sugarcane", (6.0, 7.5), (1100, 1500), {"annual"}, "High water demand crop"),
    ("cotton", (5.8, 8.0), (500, 1000), {"kharif"}, "Needs warm season & well-drained soils"),
    ("pulses", (6.0, 7.5), (400, 800), {"kharif", "rabi"}, "Low–moderate water; neutral pH"),
    ("millets", (5.5, 7.5), (300, 700), {"kharif"}, "Very resilient to low water"),
]

def _score(pH: float, rain: float, season: str, rule) -> float:
    crop, (p_lo, p_hi), (r_lo, r_hi), seasons, _ = rule
    score = 0.0
    
    # pH suitability
    if p_lo <= pH <= p_hi:
        mid = (p_lo + p_hi) / 2
        score += 1.0 - abs(pH - mid) / (p_hi - p_lo)
    
    # rainfall suitability
    if r_lo <= rain <= r_hi:
        mid = (r_lo + r_hi) / 2
        score += 1.0 - abs(rain - mid) / (r_hi - r_lo)
    
    # season match
    if season.lower() in seasons:
        score += 0.5
    
    return round(score, 3)

def recommend_crops(req: CropRecommendRequest) -> List[CropRecommendation]:
    recs = []
    for rule in CROP_RULES:
        crop, _, _, _, note = rule
        score = _score(req.soil_pH, req.rainfall_mm, req.season, rule)
        if score > 0:
            recs.append(CropRecommendation(crop=crop, score=score, rationale=note))
    recs.sort(key=lambda x: x.score, reverse=True)
    return recs[:5]
