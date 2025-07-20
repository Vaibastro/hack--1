import streamlit as st
import pandas as pd
import numpy as np

# Game Setup
st.set_page_config(page_title="Eco-Apocalypse: Air Monster War", layout="centered")

st.title("Eco-Apocalypse: The Air Monster War")

# Define actions
eco_actions = [
    "Plant Trees",
    "Use Public Transport",
    "Ban Firecrackers",
    "Switch to Solar Energy",
    "Do Nothing",
    "Car-Free Day",
    "Clean the City",
    "Eco Awareness Drive",
    "Recycle Campaign"
]

# Monster mapping function
def get_monster(aqi):
    if aqi <= 50:
        return " CleanSky"
    elif aqi <= 100:
        return "Smokeling"
    elif aqi <= 200:
        return "Fumigator"
    elif aqi <= 300:
        return "Chokethorn"
    else:
        return "Vaporgeddon"

# AQI calculator
def calculate_aqi(pm25, pm10, no2, co):
    return int(pm25 * 0.5 + pm10 * 0.3 + no2 * 0.1 + co * 30)

# Eco action effects
def apply_action(pm25, pm10, no2, co, action):
    if action == "Plant Trees":
        pm25 -= 30
        no2 -= 10
    elif action == "Use Public Transport":
        pm10 -= 20
        co -= 0.3
    elif action == "Ban Firecrackers":
        pm25 -= 50
        pm10 -= 40
    elif action == "Switch to Solar Energy":
        co -= 0.5
        no2 -= 15
    elif action == "Car-Free Day":
        co -= 0.7
        pm10 -= 30
    elif action == "Clean the City":
        pm10 -= 25
    elif action == "Eco Awareness Drive":
        pm25 -= 10
        no2 -= 5
    elif action == "Recycle Campaign":
        pm10 -= 15

    # Clamp to avoid negatives
    return max(pm25, 0), max(pm10, 0), max(no2, 0), max(co, 0)

# Session state: Day & Score
if 'day' not in st.session_state:
    st.session_state.day = 1
    st.session_state.pm25 = np.random.randint(100, 250)
    st.session_state.pm10 = np.random.randint(150, 350)
    st.session_state.no2 = np.random.randint(50, 120)
    st.session_state.co = np.round(np.random.uniform(0.8, 2.5), 2)

st.header(f"Day {st.session_state.day}")

# Show pollution values
aqi = calculate_aqi(st.session_state.pm25, st.session_state.pm10, st.session_state.no2, st.session_state.co)
monster = get_monster(aqi)

st.subheader(f"Monster: {monster}")
st.write(f"**AQI:** {aqi}")
st.write(f"PM2.5: {st.session_state.pm25}, PM10: {st.session_state.pm10}, NO2: {st.session_state.no2}, CO: {st.session_state.co}")

# Player Action
action = st.selectbox("Choose an Eco Action for Today:", eco_actions)

if st.button("Apply Action & Continue ➡️"):
    # Apply action and update pollution
    pm25, pm10, no2, co = apply_action(
        st.session_state.pm25, 
        st.session_state.pm10, 
        st.session_state.no2, 
        st.session_state.co, 
        action
    )

    # Save new pollution values
    st.session_state.pm25 = pm25
    st.session_state.pm10 = pm10
    st.session_state.no2 = no2
    st.session_state.co = co

    # Next day
    st.session_state.day += 1
    st.rerun()
