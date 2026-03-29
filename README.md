# ER-Helper: AI-Powered Emergency Dispatch Assistant

## 👥 Team Members

- Celine Helene Margrethe Amandine Johnsen
- Nathanon Srisilp
- Nutt Sittichaiopas
- Wasin Promjun
- Siranut Usawasutsakorn

---

## About the Project

ER-Helper is a human-in-the-loop AI emergency dispatch assistant designed to improve emergency intake, classification, and operator response.

The system allows users to report emergencies via Telegram using text, voice, and location sharing. Voice input is transcribed using AI, then processed into a structured emergency report. The report is stored in a database and reviewed through a Streamlit dashboard, where an operator can confirm, edit, or dispatch the case. An ESP32-based hardware alert system provides real-time visual notification.

---

## Core Features

- Telegram-based emergency reporting
- Voice-to-text transcription
- AI-based emergency extraction
- Human-in-the-loop verification
- Streamlit dashboard
- MongoDB history storage
- ESP32 LED alert integration

---

## Full Workflow

```text
User (Telegram)
   ↓
Text / Voice / Location Input
   ↓
Speech-to-Text (if voice)
   ↓
AI Extraction of Emergency Data
   ↓
Structured Report
   ↓
Backend API
   ↓
Database Storage (Pending)
   ↓
Streamlit Dashboard
   ↓
Human Operator Review
   ↓
Confirm / Edit / Dispatch
   ↓
Database Update + History Storage
   ↓
ESP32 Alert