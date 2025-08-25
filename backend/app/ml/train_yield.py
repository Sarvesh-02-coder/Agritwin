import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from catboost import CatBoostRegressor
import joblib
from pathlib import Path
import numpy as np

# Paths
DATA_PATH = Path(__file__).resolve().parents[0] / "data" / "soil_data.csv"
MODEL_PATH = Path(__file__).resolve().parents[0] / "artifacts" / "yield_model.pkl"

print(f"📂 Loading data from: {DATA_PATH}")

# Load dataset
data = pd.read_csv(DATA_PATH)

# Fix column names (strip spaces)
data.columns = data.columns.str.strip()
print(f"✅ Columns in dataset: {list(data.columns)}")

# Fill missing values for numeric features
if "Area" in data.columns:
    data["Area"] = data["Area"].fillna(data["Area"].median())
if "Production" in data.columns:
    data["Production"] = data["Production"].fillna(data["Production"].median())

# Target variable
target = "Yield"

# Features
features = ["State", "District", "Crop", "Crop_Year", "Season", "Area", "Production"]

# Prepare X and y
X = data[features].copy()
y = data[target].copy()

# Categorical columns
cat_cols = ["State", "District", "Crop", "Season"]

# Convert categorical columns to string and fill NaNs
for col in cat_cols:
    X[col] = X[col].fillna("Unknown").astype(str)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Print number of rows
print(f"📊 Total rows in dataset: {X.shape[0]}")
print(f"📈 Number of training rows: {X_train.shape[0]}")
print(f"📉 Number of testing rows: {X_test.shape[0]}")

# Define CatBoost model
model = CatBoostRegressor(
    iterations=1000,
    learning_rate=0.05,
    depth=8,
    l2_leaf_reg=3,
    random_seed=42,
    loss_function="RMSE",
    eval_metric="RMSE",
    verbose=100,
    early_stopping_rounds=50
)

# Fit model
model.fit(
    X_train, y_train,
    eval_set=(X_test, y_test),
    cat_features=cat_cols
)

# Predictions
y_pred = model.predict(X_test)

# Metrics
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
accuracy = r2 * 100  # Treat R² as "accuracy" in percentage

print("\n✅ CatBoost Model trained (FULL dataset)")
print(f"📊 R^2 score: {r2:.3f}")
print(f"📊 Accuracy: {accuracy:.2f}%")
print(f"📉 MAE: {mae:.2f}")
print(f"📉 RMSE: {rmse:.2f}")

# Save model
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_PATH)
print(f"\n💾 Model saved to: {MODEL_PATH}")
