from pathlib import Path
import joblib
import pandas as pd

# Path to trained model
MODEL_PATH = Path(__file__).resolve().parent / "artifacts" / "yield_model.pkl"

def _ensure_model():
    """
    Ensure that a trained model exists and load it.
    """
    if not MODEL_PATH.exists():
        raise RuntimeError("❌ Model not trained. Run train_yield.py first.")
    return joblib.load(MODEL_PATH)


def predict_row(
    *,
    state: str,
    district: str,
    crop: str,
    season: str,
    crop_year: int,
    area: float,
    production: float,
    weather: dict,
    soil: dict
) -> float:
    """
    Predict yield for a single row of inputs using trained CatBoost model.

    Parameters
    ----------
    state, district, crop, season : str
        Profile and crop info
    crop_year : int
        Year of cultivation
    area, production : float
        Farm area & past production
    weather : dict
        Must contain rainfall_7d_total, temp_7d_avg, humidity_7d_avg
    soil : dict
        Must contain pH, organic_carbon_pct, sand_pct, silt_pct, clay_pct
    """

    model = _ensure_model()

    row = {
        "State": state,
        "District": district,
        "Crop": crop,
        "Crop_Year": crop_year,
        "Season": season,
        "Area": area,
        "Production": production,
        "state_profile": state,
        "district_profile": district,
        "rainfall_7d_total": weather.get("rainfall_7d_total", 0.0),
        "temp_7d_avg": weather.get("temp_7d_avg", 0.0),
        "humidity_7d_avg": weather.get("humidity_7d_avg", 0.0),
        "soil_ph": soil.get("pH", 7.0),
        "soil_soc": soil.get("organic_carbon_pct", 0.5),
        "soil_sand": soil.get("sand_pct", 33.0),
        "soil_silt": soil.get("silt_pct", 33.0),
        "soil_clay": soil.get("clay_pct", 34.0),
    }

    # Convert row into DataFrame
    df = pd.DataFrame([row])

    # 🔹 Keep preprocessing consistent with training
    cat_cols = ["State", "District", "Crop", "Season", "state_profile", "district_profile"]
    for c in cat_cols:
        df[c] = df[c].fillna("Unknown").astype(str)

    num_cols = [c for c in df.columns if c not in cat_cols]
    for c in num_cols:
        df[c] = df[c].fillna(0)

    # Predict
    y_pred = model.predict(df)[0]
    return float(y_pred)
