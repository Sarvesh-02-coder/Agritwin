from typing import Dict, List
from math import isfinite
from app.models.pydantic_schemas import (
    FertilizerRequest, FertilizerAdvice, FertilizerDose
)

# Recommended Dose (RDF) per crop in kg/ha of N-P2O5-K2O
RDF_BY_CROP: Dict[str, Dict[str, float]] = {
    "rice":     {"N": 100, "P2O5": 60, "K2O": 40},
    "wheat":    {"N": 120, "P2O5": 60, "K2O": 40},
    "maize":    {"N": 150, "P2O5": 75, "K2O": 60},
    "cotton":   {"N": 150, "P2O5": 60, "K2O": 60},
    "pulses":   {"N": 25,  "P2O5": 50, "K2O": 0},
    "sugarcane":{"N": 250, "P2O5": 115,"K2O": 115},  # annual
    "millets":  {"N": 60,  "P2O5": 40, "K2O": 20},
}

# Soil test category multipliers (simple, explainable)
LEVEL_FACTOR = {"low": 1.2, "medium": 1.0, "high": 0.8}

# Fertilizer nutrient contents (%)
FERTS = {
    "Urea": {"N": 46.0},
    "DAP":  {"N": 18.0, "P2O5": 46.0},
    "SSP":  {"P2O5": 16.0},             # also supplies S ~12% (not modeled here)
    "MOP":  {"K2O": 60.0},              # Muriate of Potash
}

def _safe_round(x: float, nd: int = 1) -> float:
    return round(x, nd) if isfinite(x) else 0.0

def _adjust_for_soil_levels(rdf: Dict[str, float], req: FertilizerRequest) -> Dict[str, float]:
    n = rdf["N"]   * LEVEL_FACTOR.get(req.soil_N_level, 1.0)
    p = rdf["P2O5"]* LEVEL_FACTOR.get(req.soil_P_level, 1.0)
    k = rdf["K2O"] * LEVEL_FACTOR.get(req.soil_K_level, 1.0)
    return {"N": n, "P2O5": p, "K2O": k}

def _bias_for_yield_target(adjusted: Dict[str, float], yield_target: float | None) -> Dict[str, float]:
    # very light linear bias: +5% N for each +1 t/ha beyond an arbitrary 4 t/ha baseline, capped at +20%
    if yield_target and yield_target > 0:
        bias = min(max((yield_target - 4.0) * 0.05, -0.1), 0.2)
        adjusted["N"] *= (1.0 + bias)
    return adjusted

def _choose_P_source(p_need: float, soil_P_level: str) -> str:
    # If P need substantial or soil P low -> DAP; else SSP (cheaper, adds S)
    if p_need >= 40 or soil_P_level == "low":
        return "DAP"
    return "SSP"

def _split_n_schedule(crop: str) -> List[str]:
    c = crop.lower()
    if c == "rice":
        return [
            "Apply 50% of N + full P & K as basal at transplanting/sowing.",
            "Apply 25% N at active tillering (~20–25 DAT).",
            "Apply 25% N at panicle initiation (~45 DAT).",
        ]
    if c == "wheat":
        return [
            "Apply 50% N + full P & K as basal at sowing.",
            "Apply 50% N at first irrigation (CRI stage ~20–25 DAS).",
        ]
    if c == "maize":
        return [
            "Apply 30–40% N + full P & K as basal at sowing.",
            "Apply remaining N in 2 splits at 25–30 DAS and 45–50 DAS.",
        ]
    if c == "sugarcane":
        return [
            "Split N in 3–4 equal doses during early growth; apply full P & K at planting.",
        ]
    # generic
    return [
        "Apply full P & K as basal.",
        "Split N: half basal, remainder in 1–2 splits during peak vegetative growth.",
    ]

def get_fertilizer_advice(req: FertilizerRequest) -> FertilizerAdvice:
    crop_key = req.crop.strip().lower()
    if crop_key not in RDF_BY_CROP:
        # default to a moderate profile if unknown crop
        base = {"N": 90, "P2O5": 45, "K2O": 30}
        rationale = [f"Crop '{req.crop}' not found in preset table; using a moderate default."]
    else:
        base = RDF_BY_CROP[crop_key]
        rationale = [f"Using RDF for {req.crop}: {int(base['N'])}-{int(base['P2O5'])}-{int(base['K2O'])} kg/ha."]

    # Adjust for soil test categories
    adj = _adjust_for_soil_levels(base, req)
    rationale.append(
        f"Soil levels N={req.soil_N_level}, P={req.soil_P_level}, K={req.soil_K_level} → "
        f"adjusted to ~N {int(adj['N'])}, P2O5 {int(adj['P2O5'])}, K2O {int(adj['K2O'])} kg/ha."
    )

    # Light bias for yield target
    adj = _bias_for_yield_target(adj, req.yield_target)
    if req.yield_target:
        rationale.append(f"Yield target {req.yield_target} t/ha → slight N bias applied.")

    # Safety/cautions for pH
    cautions: List[str] = []
    if req.soil_pH is not None:
        if req.soil_pH < 5.5:
            cautions.append("Soil is acidic (pH < 5.5): consider liming and prefer SSP over DAP; avoid ammoniacal N on surface.")
        elif req.soil_pH > 8.0:
            cautions.append("Soil is alkaline (pH > 8.0): band P; consider gypsum if sodicity issues; avoid urea surface losses.")

    # Decide P source
    p_source = _choose_P_source(adj["P2O5"], req.soil_P_level)

    # Compute P fertilizer
    fert_plan: List[FertilizerDose] = []
    per_ha = {"N": adj["N"], "P2O5": adj["P2O5"], "K2O": adj["K2O"]}
    area = req.area_ha

    # 1) Meet P with DAP or SSP
    p_fert_kg_per_ha = 0.0
    n_from_p_source = 0.0
    if p_source == "DAP":
        if FERTS["DAP"]["P2O5"] > 0:
            p_fert_kg_per_ha = per_ha["P2O5"] / (FERTS["DAP"]["P2O5"] / 100.0)
            n_from_p_source = p_fert_kg_per_ha * (FERTS["DAP"]["N"] / 100.0)
        fert_plan.append(
            FertilizerDose(
                name="DAP",
                per_ha_kg=_safe_round(p_fert_kg_per_ha),
                total_kg=_safe_round(p_fert_kg_per_ha * area),
                contributes={"N": _safe_round(n_from_p_source), "P2O5": per_ha["P2O5"]}
            )
        )
    else:  # SSP
        if FERTS["SSP"]["P2O5"] > 0:
            p_fert_kg_per_ha = per_ha["P2O5"] / (FERTS["SSP"]["P2O5"] / 100.0)
        fert_plan.append(
            FertilizerDose(
                name="SSP",
                per_ha_kg=_safe_round(p_fert_kg_per_ha),
                total_kg=_safe_round(p_fert_kg_per_ha * area),
                contributes={"P2O5": per_ha["P2O5"]}
            )
        )

    # 2) Meet K with MOP
    mop_per_ha = 0.0
    if per_ha["K2O"] > 0 and FERTS["MOP"]["K2O"] > 0:
        mop_per_ha = per_ha["K2O"] / (FERTS["MOP"]["K2O"] / 100.0)
        fert_plan.append(
            FertilizerDose(
                name="MOP",
                per_ha_kg=_safe_round(mop_per_ha),
                total_kg=_safe_round(mop_per_ha * area),
                contributes={"K2O": per_ha["K2O"]}
            )
        )

    # 3) Meet remaining N with Urea
    n_need_after_p = max(per_ha["N"] - n_from_p_source, 0.0)
    urea_per_ha = 0.0
    if n_need_after_p > 0 and FERTS["Urea"]["N"] > 0:
        urea_per_ha = n_need_after_p / (FERTS["Urea"]["N"] / 100.0)
        fert_plan.append(
            FertilizerDose(
                name="Urea",
                per_ha_kg=_safe_round(urea_per_ha),
                total_kg=_safe_round(urea_per_ha * area),
                contributes={"N": _safe_round(n_need_after_p)}
            )
        )

    # Totals
    total = {
        "N": _safe_round(per_ha["N"] * area),
        "P2O5": _safe_round(per_ha["P2O5"] * area),
        "K2O": _safe_round(per_ha["K2O"] * area),
    }

    # Application schedule (by crop)
    schedule = _split_n_schedule(crop_key)

    # Rationale additions
    rationale.append(
        f"P source chosen: {p_source} (heuristic: soil P level={req.soil_P_level}, P need={_safe_round(per_ha['P2O5'])} kg/ha)."
    )
    if n_from_p_source > 0:
        rationale.append(f"Accounting for N from DAP: ~{_safe_round(n_from_p_source)} kg N/ha.")
    rationale.append("Remaining N balanced with Urea; K supplied via MOP.")

    return FertilizerAdvice(
        per_ha_NPK_kg={k: _safe_round(v) for k, v in per_ha.items()},
        total_NPK_kg=total,
        fertilizer_plan=fert_plan,
        application_schedule=schedule,
        cautions=cautions,
        rationale=rationale,
    )
