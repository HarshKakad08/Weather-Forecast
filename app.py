import streamlit as st
from utils import get_weather, get_forecast
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="🌌 Weather Forecast", layout="centered")

# --- Dark Theme Styling ---
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
            color: #f5f5f5;
        }
        .title {
            font-size: 2.5rem;
            text-align: center;
            color: #f1c40f;
            margin-bottom: 10px;
        }
        .subtext {
            text-align: center;
            color: #bdc3c7;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        .card {
            background-color: #1c1f26;
            padding: 1.5rem;
            border-radius: 1rem;
            box-shadow: 0 0 15px rgba(241, 196, 15, 0.15);
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown('<div class="title">🌌 Weather Forecast</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Enter a city name to get live and 5-day forecast</div>', unsafe_allow_html=True)

# --- Add unit toggle ---
unit = st.radio("Select Temperature Unit", ("Celsius (°C)", "Fahrenheit (°F)"))
units_code = "metric" if unit.startswith("Celsius") else "imperial"
temp_unit_symbol = "°C" if units_code == "metric" else "°F"
speed_unit = "m/s" if units_code == "metric" else "mph"

# --- Input (No label) ---
city = st.text_input("", placeholder="🌍 Enter city name (e.g., Tokyo, Delhi, Paris)")

if city:
    weather = get_weather(city, units=units_code)
    forecast = get_forecast(city, units=units_code)

    if weather:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"### 📍 {city.title()}")

        col1, col2, col3 = st.columns(3)
        col1.metric("🌡️ Temp", f"{weather['Temperature']} {temp_unit_symbol}")
        col2.metric("💧 Humidity", f"{weather['Humidity']}%")
        col3.metric("🌬️ Wind", f"{weather['Wind Speed']} {speed_unit}")

        # Description and alert
        st.markdown(f"<p style='color:#ecf0f1'><b>📝 Description:</b> {weather['Description'].capitalize()}</p>", unsafe_allow_html=True)

        if weather.get("Alert"):
            st.markdown(f"<p style='color:#f39c12; font-weight:bold;'>⚠️ {weather['Alert']}</p>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        if forecast:
            st.markdown("### 📅 5-Day Forecast")
            cols = st.columns(5)
            for i, col in enumerate(cols):
                day = forecast['days'][i]
                full_date = forecast['full_dates'][i]
                temp = forecast['temps'][i]
                icon = forecast['icons'][i]
                col.markdown(f"**{day}, {full_date}**")
                col.markdown(f"{icon}  {temp} {temp_unit_symbol}")
    else:
        st.error("❌ Could not fetch weather data. Check city name or API key.")
