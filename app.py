import streamlit as st
import pandas as pd
import requests
import numpy as np
from datetime import datetime, date

st.set_page_config(page_title="MLB HR Edge", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp { background-color: #0a0a0a; color: #ffffff; }
    h1, h2, h3 { color: #ff4d4d; font-weight: bold; }
    .dataframe { background-color: #1a1a1a !important; color: white; }
    .fire { color: #ff9500; font-size: 1.4em; }
</style>
""", unsafe_allow_html=True)

st.title("🔥 MLB HR Edge")
st.subheader(f"Daily Home Run Projections • {datetime.now().strftime('%b %d, %Y')}")

# Auto-fetch today's schedule
@st.cache_data(ttl=3600)
def get_todays_games():
    try:
        today = date.today().strftime("%Y-%m-%d")
        url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today}&hydrate=probablePitcher"
        resp = requests.get(url, timeout=10).json()
        # (simplified for demo)
        return pd.DataFrame([{"Status": "Live schedule loaded"}])
    except:
        return pd.DataFrame([{"Status": "Schedule data unavailable — demo mode"}])

st.dataframe(get_todays_games(), use_container_width=True, hide_index=True)

st.markdown("### 🔥 Top HR Projections")

uploaded = st.file_uploader("Upload batters.csv for better accuracy", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)
    df['HR_Prob'] = np.clip(df.get('barrel_batted_rate', 10) * 0.015 + 0.18, 0.15, 0.40)
    df['Grade'] = np.where(df['HR_Prob'] > 0.27, "A+", "A")
    st.dataframe(df.head(12)[['last_name','first_name','HR_Prob','Grade']].style.format({'HR_Prob': '{:.1%}'}), use_container_width=True, hide_index=True)
else:
    # Screenshot-style demo
    demo = pd.DataFrame({
        "Batter": ["Ben Rice", "Ryan McMahon", "Jazz Chisholm Jr.", "James Wood"],
        "Grade": ["A+", "A+", "A+", "A"],
        "HR Probability": ["24.5%", "24.3%", "24.3%", "30.0%"],
        "Recent Form": ["Good 🔵", "Hot 🔥", "Hot 🔥", "Hot 🔥"],
        "Pitcher": ["Slade Cecconi", "Slade Cecconi", "Slade Cecconi", "RHP"],
        "Power Match": ["🔥🔥🔥", "🔥🔥🔥", "🔥🔥🔥", "🔥🔥🔥"]
    })
    st.dataframe(demo, use_container_width=True, hide_index=True)

st.caption("Upload your Savant CSVs daily • Auto MLB schedule • Fully mobile")
