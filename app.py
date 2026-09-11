"""
app.py
------
Dashboard for the AI-Based Manganese Reserve & Production Shortfall Predictor.
Run with: streamlit run app.py
"""

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------------------
# STEP 1: Page setup
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Manganese Reserve & Shortfall Predictor",
    page_icon="⛏️",
    layout="wide",
)

# --- Visual theme: fonts, spacing, and cleanup of default Streamlit chrome ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #3B2A1E !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

hr {
    border: none;
    border-top: 1px solid #C9B994;
    margin: 1.5rem 0;
}

div[data-testid="stMetric"] {
    background-color: #EADFC2;
    border: 1px solid #C9B994;
    border-radius: 6px;
    padding: 12px 16px;
}

div[data-testid="stMetricLabel"] {
    color: #6B4226;
}

section[data-testid="stSidebar"] {
    background-color: #EADFC2;
    border-right: 1px solid #C9B994;
}
</style>
""", unsafe_allow_html=True)

st.title("Manganese Reserve & Shortfall Predictor")
st.markdown(
    "<p style='color:#6B4226; font-size:1rem; margin-top:-10px;'>"
    "AI-assisted monitoring for manganese ore output and production risk"
    "</p>",
    unsafe_allow_html=True,
)
st.markdown("<hr>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# STEP 2: Load data + trained models
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/manganese_data.csv", parse_dates=["date"])

@st.cache_resource
def load_models():
    reserve_model = joblib.load("model/reserve_model.pkl")
    risk_model = joblib.load("model/risk_model.pkl")
    return reserve_model, risk_model

df = load_data()
reserve_model, risk_model = load_models()

FEATURES = [
    "vegetation_index",
    "soil_moisture_pct",
    "land_temperature_c",
    "equipment_downtime_hours",
    "blasting_delay_hours",
    "weather_delay_hours",
]

# ---------------------------------------------------------------------------
# STEP 3: Sidebar controls
# ---------------------------------------------------------------------------
st.sidebar.header("Controls")
selected_mine = st.sidebar.selectbox("Select mine", df["mine_name"].unique())
mine_df = df[df["mine_name"] == selected_mine].sort_values("date")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Data note:** Satellite indices (vegetation, soil moisture, land "
    "temperature) are simulated here using realistic value ranges. In "
    "production, this pipeline would pull live values from Google Earth "
    "Engine / Sentinel-2 for the same coordinates."
)

# ---------------------------------------------------------------------------
# STEP 4: Top row -- map + key metrics
# ---------------------------------------------------------------------------
col_map, col_metrics = st.columns([1, 1.2])

with col_map:
    st.subheader("Mine Location")
    map_df = df.drop_duplicates("mine_name")[["mine_name", "latitude", "longitude"]]
    fig_map = px.scatter_geo(
        map_df,
        lat="latitude",
        lon="longitude",
        hover_name="mine_name",
        scope="asia",
        height=350,
    )
    fig_map.update_geos(
        showland=True, landcolor="rgb(229, 220, 200)",
        showcountries=True, countrycolor="rgb(150, 130, 110)",
        showsubunits=True, subunitcolor="rgb(200, 185, 160)",
        lataxis_range=[15, 28], lonaxis_range=[72, 90],
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

with col_metrics:
    st.subheader("Latest Prediction")
    latest_row = mine_df.iloc[[-1]]
    predicted_output = reserve_model.predict(latest_row[FEATURES])[0]
    risk_proba = risk_model.predict_proba(latest_row[FEATURES])[0][1] * 100

    m1, m2, m3 = st.columns(3)
    m1.metric("Predicted Output Today", f"{predicted_output:.0f} tons")
    m2.metric("Shortfall Risk", f"{risk_proba:.0f}%")
    m3.metric("Avg Downtime (last 7d)", f"{mine_df['equipment_downtime_hours'].tail(7).mean():.1f} hrs")

    # --- AI-generated corrective action suggestion ---
    st.markdown("#### Suggested Action")

    top_factor_idx = risk_model.feature_importances_.argmax()
    top_factor_name = FEATURES[top_factor_idx].replace("_", " ").title()
    top_factor_value = latest_row[FEATURES[top_factor_idx]].values[0]

    if risk_proba > 70:
        st.error(
            f"**HIGH RISK ({risk_proba:.0f}%)** — This mine shows a high "
            f"probability of a production shortfall today. The strongest "
            f"contributing factor is **{top_factor_name}**, currently at "
            f"**{top_factor_value:.2f}**. \n\n"
            f"**Recommended action:** Reschedule blasting to a lower-delay "
            f"window, reassign standby equipment to this site immediately, "
            f"and flag this mine for priority review by the operations team."
        )
    elif risk_proba > 40:
        st.warning(
            f"**MODERATE RISK ({risk_proba:.0f}%)** — Conditions suggest a "
            f"growing chance of shortfall if left unaddressed. "
            f"**{top_factor_name}** (currently **{top_factor_value:.2f}**) "
            f"is the leading contributor to this risk score. \n\n"
            f"**Recommended action:** Monitor equipment downtime closely "
            f"over the next 48 hours and pre-stage backup machinery in case "
            f"conditions worsen."
        )
    else:
        st.success(
            f"**LOW RISK ({risk_proba:.0f}%)** — Current conditions at this "
            f"mine are stable, with **{top_factor_name}** as the most "
            f"closely watched factor. \n\n"
            f"**Recommended action:** No intervention needed. Continue "
            f"routine monitoring."
        )

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# STEP 5: Trend chart -- predicted vs actual output over the last 60 days
# ---------------------------------------------------------------------------
st.subheader("Ore Output Trend (Last 60 Days)")
recent = mine_df.tail(60).copy()
recent["predicted_output"] = reserve_model.predict(recent[FEATURES])

fig_trend = px.line(
    recent,
    x="date",
    y=["ore_extracted_tons", "predicted_output"],
    labels={"value": "Tons", "date": "Date", "variable": "Series"},
    color_discrete_sequence=["#6B4226", "#B08D57"],
)
fig_trend.for_each_trace(
    lambda t: t.update(name={"ore_extracted_tons": "Actual", "predicted_output": "AI Predicted"}[t.name])
)
fig_trend.update_layout(
    plot_bgcolor="#F5EDDA",
    paper_bgcolor="#F5EDDA",
    font_color="#3B2A1E",
)
st.plotly_chart(fig_trend, use_container_width=True)

# ---------------------------------------------------------------------------
# STEP 6: Feature importance -- shows judges WHY the AI predicts what it does
# ---------------------------------------------------------------------------
st.subheader("What's Driving the AI's Prediction?")
importance_df = pd.DataFrame({
    "Factor": FEATURES,
    "Importance": risk_model.feature_importances_,
}).sort_values("Importance", ascending=True)

fig_importance = px.bar(
    importance_df, x="Importance", y="Factor", orientation="h",
    labels={"Importance": "Influence on Shortfall Risk"},
    color_discrete_sequence=["#6B4226"],
)
fig_importance.update_layout(
    plot_bgcolor="#F5EDDA",
    paper_bgcolor="#F5EDDA",
    font_color="#3B2A1E",
)
st.plotly_chart(fig_importance, use_container_width=True)

st.caption(
    "This chart shows which factors the AI model weighs most heavily when "
    "predicting shortfall risk."
)
