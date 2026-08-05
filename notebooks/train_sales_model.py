from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# -------------------------------------------------
# Project Paths
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "Superstore Dataset.xlsx"

MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "sales_model.pkl"

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------

print("Loading dataset...")

df = pd.read_excel(
    DATA_PATH,
    sheet_name="Orders"
)

print(f"Dataset Shape: {df.shape}")

# -------------------------------------------------
# Select Features
# -------------------------------------------------

features = [
    "Category",
    "Region",
    "Segment",
    "Quantity",
    "Discount"
]

target = "Sales"

X = df[features]

y = df[target]

# -------------------------------------------------
# Preprocessing
# -------------------------------------------------

categorical_features = [
    "Category",
    "Region",
    "Segment"
]

numeric_features = [
    "Quantity",
    "Discount"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features,
        ),
        (
            "num",
            "passthrough",
            numeric_features,
        ),
    ]
)

# -------------------------------------------------
# Model
# -------------------------------------------------

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "model",
            RandomForestRegressor(
                n_estimators=200,
                random_state=42,
            ),
        ),
    ]
)

# -------------------------------------------------
# Train Test Split
# -------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
)

print("Training model...")

model.fit(X_train, y_train)

# -------------------------------------------------
# Predictions
# -------------------------------------------------

predictions = model.predict(X_test)

# -------------------------------------------------
# Evaluation
# -------------------------------------------------

mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)

print("\nModel Performance")
print("-" * 40)
print(f"MAE : {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R²  : {r2:.4f}")

# -------------------------------------------------
# Save Model
# -------------------------------------------------

joblib.dump(model, MODEL_PATH)

print("\nModel saved successfully!")
print(f"Location: {MODEL_PATH}")

print("\nTraining Completed Successfully!")