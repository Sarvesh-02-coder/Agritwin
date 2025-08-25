import pandas as pd
from pathlib import Path
from app.models.pydantic_schemas import PestAlertRequest, PestDiseaseAlert
import os
DATA_DIR = Path(__file__).resolve().parents[1] / "ml" / "data"
PEST_CSV = DATA_DIR / "pest_disease.csv"
PEST_DF = pd.read_csv(PEST_CSV)

def get_pest_alerts(req: PestAlertRequest):
    crop_key = req.crop.strip().lower()
    season_key = req.season.strip().lower()
    alerts = []

    for _, row in PEST_DF.iterrows():
        if row["crop"].lower() != crop_key: 
            continue
        if row["season"].lower() != season_key: 
            continue
        
        # Check temp and humidity overlap
        if row["temp_min"] <= req.temp_c <= row["temp_max"] and \
           row["humidity_min"] <= req.humidity <= row["humidity_max"]:
            risk = "High"
        else:
            risk = "Low"

        alerts.append(
            PestDiseaseAlert(
                pest=row["pest"],
                disease=row["disease"],
                risk=risk,
                note=row.get("note", None)
            )
        )
    return alerts
