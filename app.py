import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5001")

st.set_page_config(page_title="ER-Helper Dispatch Dashboard", layout="wide")
st_autorefresh(interval=3000, key="dispatch_refresh")


def get_reports(status=None):
    params = {}
    if status:
        params["status"] = status
    response = requests.get(f"{BACKEND_URL}/api/reports", params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def update_report(report_id, payload):
    response = requests.put(
        f"{BACKEND_URL}/api/reports/{report_id}",
        json=payload,
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def set_live_state(state):
    response = requests.get(
        f"{BACKEND_URL}/api/set-status",
        params={"state": state},
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def get_live_state():
    response = requests.get(f"{BACKEND_URL}/api/alert-status", timeout=10)
    response.raise_for_status()
    return response.json().get("state", "unknown")


def severity_color(severity):
    s = str(severity).lower()
    if "high" in s or "critical" in s:
        return "#ff4b4b"
    if "medium" in s:
        return "#f0ad4e"
    return "#4caf50"


def pill(text, color):
    return (
        f'<span style="background-color:{color};color:white;'
        f'padding:6px 12px;border-radius:999px;font-size:12px;'
        f'font-weight:600;display:inline-block;">{text}</span>'
    )


def safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


all_reports = get_reports()
pending_reports = [r for r in all_reports if str(r.get("status", "")).lower() == "pending"]
history_reports = [r for r in all_reports if str(r.get("status", "")).lower() != "pending"]
live_state = get_live_state()

st.markdown(
    """
    <style>
    .main-title {
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 6px;
    }
    .subtle {
        color: #9aa0a6;
        margin-bottom: 20px;
    }
    .info-box {
        background: #16324f;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 16px;
        color: #7fc1ff;
    }
    .section-gap {
        margin-top: 30px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Live Dispatch", "Dispatch History"])

if page == "Live Dispatch":
    st.markdown('<div class="main-title">ER-Helper Dispatch Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="subtle">Live emergency monitoring • Current alert state: <b>{live_state}</b></div>',
        unsafe_allow_html=True
    )

    if not pending_reports:
        st.success("No pending emergency reports.")
    else:
        # take newest pending report
        report = pending_reports[0]

        report_id = report["id"]

        left, right = st.columns([1.1, 1])

        with left:
            st.header("AI Analysis (Editable)")
            st.markdown(
                '<div class="info-box">Operators can adjust the AI\'s findings before dispatching.</div>',
                unsafe_allow_html=True
            )

            location = st.text_input(
                "Location (Address):",
                value=report.get("location", "")
            )

            lat_col, lon_col = st.columns(2)
            with lat_col:
                gps_lat = st.number_input(
                    "Latitude:",
                    value=safe_float(report.get("gps_lat"), 14.0690),
                    format="%.5f"
                )
            with lon_col:
                gps_lon = st.number_input(
                    "Longitude:",
                    value=safe_float(report.get("gps_lon"), 100.6050),
                    format="%.5f"
                )

            incident_type = st.text_input(
                "Incident Type:",
                value=report.get("incident_type", "")
            )

            severity = st.text_input(
                "Severity Level:",
                value=report.get("severity", "")
            )

            injured = st.text_input(
                "Injured:",
                value=str(report.get("injured", "unknown"))
            )

            st.markdown("---")
            st.header("Dispatch Map")
            st.caption(f"Pin drop at Lat: {gps_lat}, Lon: {gps_lon}")

            map_df = pd.DataFrame([{"lat": gps_lat, "lon": gps_lon}])
            st.map(map_df)

        with right:
            st.header("Call Transcript")
            transcript = st.text_area(
                "Raw Audio/Text Transcript",
                value=report.get("transcript", ""),
                height=220
            )

            st.markdown("<br>", unsafe_allow_html=True)

            confirm = st.button(
                "Confirm Details & Dispatch Teams",
                use_container_width=True,
                type="primary"
            )

            reject = st.button(
                "Reject Report",
                use_container_width=True
            )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### Current AI Output")
            st.markdown(
                pill(report.get("severity", "unknown"), severity_color(report.get("severity", "unknown"))),
                unsafe_allow_html=True
            )
            st.markdown(f"**Source:** {report.get('source', 'unknown')}")
            st.markdown(f"**Confidence:** {report.get('confidence', 'unknown')}")

            if confirm:
                update_report(
                    report_id,
                    {
                        "location": location,
                        "gps_lat": gps_lat,
                        "gps_lon": gps_lon,
                        "incident_type": incident_type,
                        "severity": severity,
                        "injured": injured,
                        "transcript": transcript,
                        "status": "confirmed"
                    }
                )
                set_live_state("confirmed")
                st.success("Report confirmed and dispatched.")
                st.rerun()

            if reject:
                update_report(
                    report_id,
                    {
                        "location": location,
                        "gps_lat": gps_lat,
                        "gps_lon": gps_lon,
                        "incident_type": incident_type,
                        "severity": severity,
                        "injured": injured,
                        "transcript": transcript,
                        "status": "rejected"
                    }
                )
                set_live_state("idle")
                st.warning("Report rejected.")
                st.rerun()

elif page == "Dispatch History":
    st.markdown('<div class="main-title">Dispatch History</div>', unsafe_allow_html=True)

    if not history_reports:
        st.info("No dispatch history yet.")
    else:
        table_rows = []
        for r in history_reports:
            table_rows.append(
                {
                    "Timestamp": r.get("created_at", ""),
                    "Address": r.get("location", ""),
                    "Lat": r.get("gps_lat", ""),
                    "Lon": r.get("gps_lon", ""),
                    "Type": r.get("incident_type", ""),
                    "Severity": r.get("severity", ""),
                    "Status": r.get("status", ""),
                    "Transcript": r.get("transcript", ""),
                }
            )

        df = pd.DataFrame(table_rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.header("Detailed Incident Logs")

        for r in history_reports:
            title = f"{r.get('created_at', '')} - {r.get('incident_type', '')} at {r.get('location', '')}"
            with st.expander(title):
                st.write(f"**Exact Coordinates:** {r.get('gps_lat', '')}, {r.get('gps_lon', '')}")
                st.write(f"**Severity:** {r.get('severity', '')}")
                st.write(f"**Status:** {r.get('status', '')}")
                st.write("**Call Transcript:**")
                st.info(r.get("transcript", ""))