import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.title("🔥 Wildfire Risk Predictor")

# ── Inputs ─────────────────────────────
st.sidebar.header("Enter Weather Details")


temp = st.sidebar.slider("Temperature (°C)", 10, 100, 35)
humidity = st.sidebar.slider("Humidity (%)", 0, 100, 30)
wind = st.sidebar.slider("Wind Speed (km/h)", 0, 80, 20)
rain_days = st.sidebar.slider("Days Since Rain", 0, 30, 10)

# ── Simple Risk Function ───────────────
def calculate_risk(temp, humidity, wind, rain_days):
    score = (
        (temp * 0.3) +
        ((100 - humidity) * 0.3) +
        (wind * 0.2) +
        (rain_days * 0.2)
    )
    return round(score / 2, 1)

risk = calculate_risk(temp, humidity, wind, rain_days)

# ── Risk Level ─────────────────────────
if risk < 20:
    level = "Low"
    color = "#2ecc71"
elif risk < 30:
    level = "Moderate"
    color = "#f39c12"
else:
    level = "High"
    color = "#e74c3c"

# ── Display ────────────────────────────
st.subheader("🔥 Risk Result")
st.write(f"Risk Score: **{risk} / 100**")
st.write(f"Risk Level: **{level}**")
st.markdown(f"<div style='background-color:{color};padding:10px;border-radius:5px;color:white;text-align:center;font-size:20px;'>{level} Risk</div>", unsafe_allow_html=True)   
upload = st.file_uploader("Upload Weather Data (CSV)", type="csv")
if upload:
    df = pd.read_csv(upload)
    st.write("📊 Uploaded Data:")
    st.dataframe(df.head())

# ── Simple Chart ───────────────────────
data = pd.DataFrame({
    "Factor": ["Temperature", "Low Humidity", "Wind", "Dry Days"],
    "Value": [temp, 100 - humidity, wind, rain_days]
})

fig = px.bar(data, x="Factor", y="Value", title="Risk Factors")
st.plotly_chart(fig)

# ── Simple Trend Graph ─────────────────
days = list(range(1, 8))
trend = [risk + np.random.randint(-5, 5) for _ in days]

trend_df = pd.DataFrame({
    "Day": days,
    "Risk": trend
})

fig2 = px.line(trend_df, x="Day", y="Risk", title="7-Day Risk Trend")
st.plotly_chart(fig2)

def risk_gauge(risk):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk,
        title = {'text': "Wildfire Risk Gauge"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "red"},
            'steps' : [
                {'range': [0, 20], 'color': "#2ecc71"},
                {'range': [20, 30], 'color': "#f39c12"},
                {'range': [30, 100], 'color': "#e74c3c"}
            ],
        }
    ))
    return fig

st.subheader("📈 Risk Gauge")
fig3 = risk_gauge(risk)
st.plotly_chart(fig3)