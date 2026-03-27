import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="ER-Helper")
st.title("ER-Helper Dispatch Dashboard")

# MOCK DATA 
EXTRACTED_ADDRESS = "Thammasat University Road, Khlong Nueng"
EXACT_LAT = 14.0690
EXACT_LON = 100.6050
INCIDENT_TYPE = "Vehicle Collision"
SEVERITY = "High (2 ER Units Recommended)"