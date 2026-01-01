import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Weather-Based Violation Recommendation",
    page_icon="🌦️",
    layout="wide"
)

st.header("🌦️ Weather-Triggered Violation Recommendation System")
st.markdown(
    "This module recommends the most likely traffic violations based on current weather conditions."
)

# -------------------------------------------------
# Load dataset from session
# -------------------------------------------------
df = st.session_state.get("df")

if df is None or df.empty:
    st.warning("Please select a dataset from the sidebar.")
    st.stop()

df = df.copy()

required_cols = ['Weather_Condition', 'Violation_Type']
df = df.dropna(subset=required_cols)

if df.empty:
    st.error("Not enough valid data for recommendations.")
    st.stop()

# -------------------------------------------------
# Weather Selection
# -------------------------------------------------
weather = st.selectbox(
    "Select Weather Condition",
    sorted(df['Weather_Condition'].unique())
)

# -------------------------------------------------
# Recommendation Logic
# -------------------------------------------------
weather_df = df[df['Weather_Condition'] == weather]

violation_counts = (
    weather_df['Violation_Type']
    .value_counts()
    .reset_index()
)

violation_counts.columns = ['Violation_Type', 'Count']

violation_counts['Probability (%)'] = (
    violation_counts['Count'] / violation_counts['Count'].sum() * 100
).round(2)

# -------------------------------------------------
# Display Recommendations
# -------------------------------------------------
st.subheader("🚦 Top Expected Violations")

top_k = st.slider("Number of recommendations", 3, 10, 5)

st.dataframe(
    violation_counts.head(top_k),
    use_container_width=True
)

# -------------------------------------------------
# AI Insight
# -------------------------------------------------
top_violation = violation_counts.iloc[0]['Violation_Type']

st.markdown("### 🧠 AI Insight")
st.info(
    f"Under **{weather}** conditions, **{top_violation}** is the most frequent violation. "
    "Traffic authorities can prioritize monitoring and enforcement accordingly."
)


