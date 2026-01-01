import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(page_title="Risk Prediction", page_icon="🚦", layout="wide")
st.header("🚦 AI-Based Traffic Violation Risk Prediction")

# -------------------------------------------------
# Load dataset from session (sidebar)
# -------------------------------------------------
df = st.session_state.get("df")

if df is None or df.empty:
    st.warning("Please select a dataset from the sidebar.")
    st.stop()

df = df.copy()

# -------------------------------------------------
# Feature Engineering
# -------------------------------------------------
df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
df['Hour'] = df['Time'].dt.hour

required_cols = [
    'Hour',
    'Vehicle_Type',
    'Weather_Condition',
    'Penalty_Points',
    'Previous_Violations'
]

df = df.dropna(subset=required_cols)

if df.empty:
    st.error("Not enough valid data after preprocessing.")
    st.stop()

# -------------------------------------------------
# Risk Label Creation (Ground Truth)
# -------------------------------------------------
def risk_label(row):
    score = (row['Penalty_Points'] * 2) + (row['Previous_Violations'] * 3)

    if score <= 5:
        return "Low"
    elif score <= 15:
        return "Medium"
    else:
        return "High"

df['Risk_Level'] = df.apply(risk_label, axis=1)
if st.checkbox("📊 Show Risk Level Distribution"):
    st.write(df['Risk_Level'].value_counts(normalize=True))
    

# -------------------------------------------------
# Encode categorical variables
# -------------------------------------------------
encoders = {}

le_vehicle = LabelEncoder()
df['Vehicle_Type'] = le_vehicle.fit_transform(df['Vehicle_Type'])
encoders['Vehicle_Type'] = le_vehicle

le_weather = LabelEncoder()
df['Weather_Condition'] = le_weather.fit_transform(df['Weather_Condition'])
encoders['Weather_Condition'] = le_weather

le_risk = LabelEncoder()
df['Risk_Level'] = le_risk.fit_transform(df['Risk_Level'])
encoders['Risk_Level'] = le_risk

# -------------------------------------------------
# Features & Target (NO leakage, stronger context)
# -------------------------------------------------
X = df[['Hour', 'Vehicle_Type', 'Weather_Condition']]
y = df['Risk_Level']

# -------------------------------------------------
# Train ML Model
# -------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train, y_train)

accuracy = accuracy_score(y_test, model.predict(X_test))
st.success(f"Model Accuracy: {accuracy:.2f}")

# -------------------------------------------------
# Prediction UI
# -------------------------------------------------
st.subheader("🔮 Predict Violation Risk")

hour = st.slider("Hour of Day", 0, 23, 12)

vehicle = st.selectbox(
    "Vehicle Type",
    encoders['Vehicle_Type'].classes_
)

weather = st.selectbox(
    "Weather Condition",
    encoders['Weather_Condition'].classes_
)

input_df = pd.DataFrame([[
    hour,
    encoders['Vehicle_Type'].transform([vehicle])[0],
    encoders['Weather_Condition'].transform([weather])[0]
]], columns=X.columns)

# -------------------------------------------------
# Predict + Probabilities
# -------------------------------------------------
if st.button("Predict Risk"):
    pred = model.predict(input_df)[0]
    risk = encoders['Risk_Level'].inverse_transform([pred])[0]

    proba = model.predict_proba(input_df)[0]

    st.markdown("### 📊 Risk Probability Distribution")
    st.write({
        "Low Risk %": round(proba[encoders['Risk_Level'].transform(["Low"])[0]] * 100, 2),
        "Medium Risk %": round(proba[encoders['Risk_Level'].transform(["Medium"])[0]] * 100, 2),
        "High Risk %": round(proba[encoders['Risk_Level'].transform(["High"])[0]] * 100, 2),
    })

    if risk == "High":
        st.error("🚨 High Risk of Traffic Violation")
    elif risk == "Medium":
        st.warning("⚠️ Medium Risk of Traffic Violation")
    else:
        st.success("✅ Low Risk of Traffic Violation")
