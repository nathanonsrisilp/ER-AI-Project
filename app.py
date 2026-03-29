import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5000")

st.set_page_config(page_title="ER-Helper Dashboard", layout="wide")
st.title("🚑 ER-Helper Dashboard")

tab1, tab2 = st.tabs(["Pending Reports", "History"])


def get_reports(status=None):
    url = f"{BACKEND_URL}/api/reports"
    params = {}
    if status:
        params["status"] = status
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def update_report(report_id, payload):
    response = requests.put(f"{BACKEND_URL}/api/reports/{report_id}", json=payload, timeout=10)
    response.raise_for_status()
    return response.json()


with tab1:
    st.subheader("Pending Reports")
    reports = get_reports(status="pending")

    if not reports:
        st.info("No pending reports.")
    else:
        for report in reports:
            with st.expander(f"{report['incident_type']} | {report['location']} | {report['status']}"):
                incident_type = st.text_input(
                    "Incident Type", value=report["incident_type"], key=f"incident_{report['id']}"
                )
                injured = st.text_input(
                    "Injured", value=report["injured"], key=f"injured_{report['id']}"
                )
                location = st.text_input(
                    "Location", value=report["location"], key=f"location_{report['id']}"
                )
                severity_values = ["low", "medium", "high"]
                current_severity = report["severity"].lower() if report["severity"] else "medium"
                severity_index = severity_values.index(current_severity) if current_severity in severity_values else 1

                severity = st.selectbox(
                    "Severity",
                    severity_values,
                    index=severity_index,
                    key=f"severity_{report['id']}"
                )
                confidence = st.text_input(
                    "Confidence", value=report["confidence"], key=f"confidence_{report['id']}"
                )

                st.markdown("**Transcript**")
                st.write(report["transcript"])

                if report.get("gps_lat") and report.get("gps_lon"):
                    st.map(pd.DataFrame([{
                        "lat": report["gps_lat"],
                        "lon": report["gps_lon"]
                    }]))

                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("✅ Confirm", key=f"confirm_{report['id']}"):
                        update_report(report["id"], {
                            "incident_type": incident_type,
                            "injured": injured,
                            "location": location,
                            "severity": severity,
                            "confidence": confidence,
                            "status": "confirmed"
                        })
                        st.success("Report confirmed.")
                        st.rerun()

                with col2:
                    if st.button("✏️ Save Edit", key=f"edit_{report['id']}"):
                        update_report(report["id"], {
                            "incident_type": incident_type,
                            "injured": injured,
                            "location": location,
                            "severity": severity,
                            "confidence": confidence,
                            "status": "edited"
                        })
                        st.success("Report edited.")
                        st.rerun()

                with col3:
                    if st.button("🚑 Dispatch", key=f"dispatch_{report['id']}"):
                        update_report(report["id"], {
                            "incident_type": incident_type,
                            "injured": injured,
                            "location": location,
                            "severity": severity,
                            "confidence": confidence,
                            "status": "dispatched"
                        })
                        st.success("Dispatch sent.")
                        st.rerun()

with tab2:
    st.subheader("History")
    reports = get_reports()

    if not reports:
        st.info("No reports found.")
    else:
        df = pd.DataFrame(reports)
        st.dataframe(df, use_container_width=True)