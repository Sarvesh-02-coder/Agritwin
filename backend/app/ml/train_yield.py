import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from catboost import CatBoostRegressor
import joblib
from pathlib import Path
import numpy as np

from app.services.profile_service import get_active_profile
from app.services.weather_service import fetch_weather_summary
from app.services.soil_service import summarize_soil

# Paths
DATA_PATH = Path(__file__).resolve().parent / "data" / "soil_data.csv"
MODEL_PATH = Path(__file__).resolve().parent / "artifacts" / "yield_model.pkl"

print(f"📂 Loading dataset: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()

# Target variable
target = "Yield"
if target not in df.columns:
    raise RuntimeError(f"❌ '{target}' column not found in dataset!")

# Fill missing numeric values
for col in ("Area", "Production"):
    if col in df.columns:
        df[col] = df[col].fillna(df[col].median())

# 🔹 Get active profile
profile = get_active_profile()
if not profile:
    raise RuntimeError("❌ No active profile found.")

pincode = profile.get("pincode")
state = profile.get("state", "Unknown")
district = profile.get("district", "Unknown")

# 🔹 Fetch live weather & soil data
weather = fetch_weather_summary(pincode)
soil = summarize_soil(pincode)

# 🔹 Add context columns (so model learns structure)
df["state_profile"] = state
df["district_profile"] = district
df["rainfall_7d_total"] = weather.get("rainfall_7d_total", 0)
df["temp_7d_avg"] = weather.get("temp_7d_avg", 0)
df["humidity_7d_avg"] = weather.get("humidity_7d_avg", 0)
df["soil_ph"] = soil.get("pH", 7.0)
df["soil_soc"] = soil.get("organic_carbon_pct", 0.5)
df["soil_sand"] = soil.get("sand_pct", 33.0)
df["soil_silt"] = soil.get("silt_pct", 33.0)
df["soil_clay"] = soil.get("clay_pct", 34.0)

# 🔹 Feature set
features = [
    "State", "District", "Crop", "Crop_Year", "Season",
    "Area", "Production",
    "state_profile", "district_profile",
    "rainfall_7d_total", "temp_7d_avg", "humidity_7d_avg",
    "soil_ph", "soil_soc", "soil_sand", "soil_silt", "soil_clay"
]

X = df[features].copy()
y = df[target].copy()

# 🔹 Handle categorical and numeric columns
cat_cols = ["State", "District", "Crop", "Season", "state_profile", "district_profile"]
for c in cat_cols:
    X[c] = X[c].fillna("Unknown").astype(str)

num_cols = [c for c in X.columns if c not in cat_cols]
for c in num_cols:
    X[c] = X[c].fillna(0)

# 🔹 Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 🔹 Train CatBoost (tell it categorical features explicitly!)
model = CatBoostRegressor(
    iterations=1000,
    learning_rate=0.05,
    depth=8,
    l2_leaf_reg=3,
    random_seed=42,
    loss_function="RMSE",
    eval_metric="RMSE",
    early_stopping_rounds=50,
    verbose=100
)

# 👇 Important: pass cat_features=cat_cols
model.fit(X_train, y_train, eval_set=(X_test, y_test), cat_features=cat_cols)

# 🔹 Evaluate
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\n✅ Model trained successfully")
print(f"R² = {r2:.3f} | MAE = {mae:.2f} | RMSE = {rmse:.2f}")

# 🔹 Save model
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_PATH)
print(f"💾 Model saved at: {MODEL_PATH}")
