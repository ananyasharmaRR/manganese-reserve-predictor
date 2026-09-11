"""
train_model.py
---------------
WHAT THIS FILE DOES:
Reads the data we generated, and trains TWO simple AI models:
  1. A model that predicts how much ore will be extracted (a number, e.g. 210 tons)
  2. A model that predicts shortfall RISK (yes/no -- will output likely fall
     more than 20% below normal?)

WHY WE'RE DOING THIS:
This is the "AI/ML" part the problem statement literally asks for:
"analysing geological data, historical production, equipment performance, and
satellite/space technology inputs" to "predict shortfalls in production."

WHY RANDOM FOREST (not deep learning / neural networks):
Random Forest is a well-respected, industry-standard model for exactly this
kind of tabular (spreadsheet-style) data. It's simple to explain to judges
("it's like asking 100 different experts and taking the majority vote"),
trains in seconds, and doesn't need a GPU. Deep learning would be overkill
here and slower to get working -- using the RIGHT tool for the job is itself
a good answer if a judge asks "why not deep learning?"

HOW TO RUN THIS FILE:
    python train_model.py
It will print accuracy scores and save two model files into the model/ folder.
"""

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score

# ---------------------------------------------------------------------------
# STEP 1: Load the data we generated earlier
# ---------------------------------------------------------------------------
df = pd.read_csv("data/manganese_data.csv")

# These are the columns (features) the model is allowed to "look at" when
# making a prediction -- everything the satellite + operations data gives us
FEATURES = [
    "vegetation_index",
    "soil_moisture_pct",
    "land_temperature_c",
    "equipment_downtime_hours",
    "blasting_delay_hours",
    "weather_delay_hours",
]

X = df[FEATURES]

# ---------------------------------------------------------------------------
# STEP 2: Train Model 1 -- predicts exact ore output (a number)
# ---------------------------------------------------------------------------
y_output = df["ore_extracted_tons"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y_output, test_size=0.2, random_state=42
)

output_model = RandomForestRegressor(n_estimators=200, random_state=42)
output_model.fit(X_train, y_train)

predictions = output_model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"[Reserve/Output Model] Average prediction error: {mae:.2f} tons/day")

# ---------------------------------------------------------------------------
# STEP 3: Train Model 2 -- predicts shortfall risk (yes/no)
# ---------------------------------------------------------------------------
y_risk = df["shortfall_flag"]
X_train2, X_test2, y_train2, y_test2 = train_test_split(
    X, y_risk, test_size=0.2, random_state=42
)

risk_model = RandomForestClassifier(n_estimators=200, random_state=42)
risk_model.fit(X_train2, y_train2)

risk_predictions = risk_model.predict(X_test2)
accuracy = accuracy_score(y_test2, risk_predictions)
print(f"[Shortfall Risk Model] Accuracy: {accuracy * 100:.1f}%")

# ---------------------------------------------------------------------------
# STEP 4: Save both trained models so the dashboard can load them instantly
# (without retraining every time the dashboard opens)
# ---------------------------------------------------------------------------
joblib.dump(output_model, "model/reserve_model.pkl")
joblib.dump(risk_model, "model/risk_model.pkl")

print("\nSaved model/reserve_model.pkl and model/risk_model.pkl")
print("You're ready to run the dashboard now: streamlit run app.py")
