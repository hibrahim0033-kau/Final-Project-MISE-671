import json
import streamlit as st
from streamlit_lottie import st_lottie

#Page config
st.set_page_config(
    page_title="MISE 671 — Diabetes Visualization",
    page_icon="kau_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.logo('kau_logo.png')
#Pages
pages = [
    st.Page("pages/home.py",     title="Home"),
    st.Page("pages/eda.py",      title="EDA"),
    st.Page("pages/worldmap.py", title="World Map"),
]
pg = st.navigation(pages, position="sidebar", expanded=True)


# Load lottie
with open("Data center.json") as f:
    lottie_data = json.load(f)


left, center, right = st.columns([1, 2, 1])

with left:
    st.image("MISE.png", width=80)

with center:
    st_lottie(lottie_data, height=130, key="header_lottie")
    st.subheader("MISE 671 — Diabetes Data Visualization", text_alignment="center")
    st.caption("Final Project 2026 · Group 2", text_alignment="center")


with right:
    st.image("kau.png", width=360)

st.divider()



pg.run()