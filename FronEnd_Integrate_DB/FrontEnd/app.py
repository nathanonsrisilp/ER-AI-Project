import streamlit as st
import pandas as pd
import requests
import os

API_URL = os.getenv("API_URL")

st.set_page_config(layout="wide", page_title="ER-Helper")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Live Dispatch", "Dispatch History"])

incident_types = [
    "Medical Emergencies",
    "Natural Disasters",
    "Technical/Industrial Incidents",
    "Human-Caused/Security Incidents",
    "Fire-Related Incidents",
    "Other"
]

severity_levels = [
    "SEV 1: Critical incident affecting many users",
    "SEV 2: Significant issue affecting limited users",
    "SEV 3: Minor errors or system load",
    "SEV 4: Minor problem with no significant impact",
    "SEV 5: Low-level issue causing minor problems"
]

if page == "Live Dispatch":
    st.title("ER-Helper Dispatch Dashboard")

    EXTRACTED_ADDRESS = "Type Location Here"
    EXACT_LAT = 14.0690
    EXACT_LON = 100.6050

    col1, col2 = st.columns(2)

    with col1:
        st.header("AI Analysis (Editable)")
        st.info("Operators can adjust the AI's findings before dispatching.")

        address_input = st.text_input("**Location (Address):**", value=EXTRACTED_ADDRESS)
        coord_col1, coord_col2 = st.columns(2)
        with coord_col1:
            lat_input = st.number_input("**Latitude:**", value=EXACT_LAT, format="%.5f")
        with coord_col2:
            lon_input = st.number_input("**Longitude:**", value=EXACT_LON, format="%.5f")

        type_input = st.selectbox("**Incident Type:**", incident_types)

        severity_input = st.selectbox("**Severity Level:**", severity_levels)

        st.divider()

        st.header("Dispatch Map")
        st.caption(f"Pin drop at Lat: {lat_input}, Lon: {lon_input}")
        map_data = pd.DataFrame({
            'lat': [lat_input], 
            'lon': [lon_input]
        })
        st.map(map_data, zoom=14)

    with col2:
        st.header("Call Transcript")
        st.text_area(
            "Raw Audio Text",
            "AI not hear anything yet(don't forget to connect audio text here!)",
            height=200
        )
        
        st.divider()

        response_input = st.text_area("**Emergency Response**", "Input what resoucre have been used to response the incident", height=100)

        if st.button("Confirm Details & Dispatch Teams", type="primary", use_container_width=True):
            payload = {
                "Timestamp": "2026-03-28",
                "Address": address_input,
                "Lat": lat_input,
                "Lon": lon_input,
                "Type": type_input,
                "Severity": severity_input,
                "Transcript": "Live dispatch",
                "Response": response_input
            }

            requests.post(f"{API_URL}/dispatches", json=payload)

            st.success(f"Dispatch stored and sent to {address_input}")

elif page == "Dispatch History":
    st.title("Dispatch History")

    response = requests.get(f"{API_URL}/dispatches")
    data = response.json()

    if data:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.divider()

        st.subheader("Detailed Incident Logs")
        for row in data:
            with st.expander(f"{row['Timestamp']} - {row['Type']} at {row['Address']}"):
                st.write(f"**Exact Coordinates:** {row['Lat']}, {row['Lon']}")
                st.write(f"**Severity:** {row['Severity']}")
                st.write(f"**Response:** {row['Response']}")
                st.write("**Call Transcript:**")
                st.info(row['Transcript'])
    else:
        st.warning("No dispatch records found.")
