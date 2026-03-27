import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="ER-Helper")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Live Dispatch", "Dispatch History"])

# MOCK DATABASE 
mock_database = pd.DataFrame([
    {
        "Timestamp": "2026-03-27 10:15 AM",
        "Address": "Future Park Rangsit, Pathum Thani",
        "Lat": 13.9893,
        "Lon": 100.6177,
        "Type": "Medical Emergency",
        "Severity": "Medium (1 Ambulance)",
        "Transcript": "Someone collapsed near the main entrance. They are breathing but unconscious."
    },
    {
        "Timestamp": "2026-03-26 08:30 PM",
        "Address": "TU Dome Plaza, Khlong Nueng",
        "Lat": 14.0680,
        "Lon": 100.6010,
        "Type": "Fire",
        "Severity": "Critical (3 Firetrucks)",
        "Transcript": "There's heavy smoke coming from the restaurant kitchen! We need fire trucks now!"
    }
])

if page == "Live Dispatch":
    st.title("ER-Helper Dispatch Dashboard")

    # MOCK DATA 
    EXTRACTED_ADDRESS = "Thammasat University Road, Khlong Nueng"
    EXACT_LAT = 14.0690
    EXACT_LON = 100.6050
    INCIDENT_TYPE = "Vehicle Collision"
    SEVERITY = "High (2 ER Units Recommended)"

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
            
        type_input = st.text_input("**Incident Type:**", value=INCIDENT_TYPE)
        severity_input = st.text_input("**Severity Level:**", value=SEVERITY)
        
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
            "Help! There is a bad car crash on the main road near Thammasat University. Two cars hit each other and someone is bleeding. We need an ambulance right away!",
            height=200
        )
        
        st.divider()

        if st.button("Confirm Details & Dispatch Teams", type="primary", use_container_width=True):
            st.success(f"Dispatching ER units to {address_input} ({lat_input}, {lon_input}).")

elif page == "Dispatch History":
    st.title("Dispatch History")
    
    st.dataframe(mock_database, use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.subheader("Detailed Incident Logs")
    for index, row in mock_database.iterrows():
        with st.expander(f"{row['Timestamp']} - {row['Type']} at {row['Address']}"):
            st.write(f"**Exact Coordinates:** {row['Lat']}, {row['Lon']}")
            st.write(f"**Severity:** {row['Severity']}")
            st.write("**Call Transcript:**")
            st.info(row['Transcript'])