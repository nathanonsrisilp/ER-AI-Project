# ER-Helper: AI-Powered Emergency Dispatch Assistant

## About the Project
Emergency Responder (ER) Call Centers currently use a lot of time gaining information directly from the caller. During high stress situations, this manual data entry can causes delays, making the caller feel that the ER took too long to respond and losing critical time to provide data for the call center. 

**ER-Helper** is an AI pipeline designed to automate the intake process. The system evaluates the situation based on caller information by capturing keywords to evaluate the amount of ER needs. The main goal is to help allocate ER resources and manpower significantly faster.

## Core Features
* **Real Time Transcription:** Uses a Speech to Text to instantly transcribe the emergency call.
* **LLM Keyword Extraction:** An LLM extracts keywords from the caller speaking to evaluate the situation and identifying the location, type of incident, and size of the incident.
* **Verification Dashboard:** Instead of typing from scratch, the Call Center operator simply confirms the information or adjusts it as they see fit.
* **Instant GPS Dispatch:** Once the operator confirms the details, the system notifies the ER and just gives the location so they can go to the destination quickly. 

## System Workflow 
1. **Intake:** The caller calls the Call Center and tells them about the incident.
2. **AI Processing:** The system processes the audio. The LLM extracts the location, incident type, and severity.
3. **Human in the Loop:** The Call Center operator reviews the AI-generated summary on their dashboard and confirms the data.
4. **Dispatch:** The verified GPS location and incident details are sent directly to the ER unit's device.

## Stakeholders
* **Callers:** Need fast, frictionless communication during emergencies.
* **ER Call Center Operators:** Need to reduce time spent manually logging information.
* **Emergency Responders:** Need GPS locations to navigate to the scene.

Current UI page
<img width="1906" height="912" alt="Screenshot 2026-03-27 201917" src="https://github.com/user-attachments/assets/baf104a8-a525-4b66-aa21-0cf130293807" />

<img width="1902" height="911" alt="Screenshot 2026-03-27 201931" src="https://github.com/user-attachments/assets/622a2655-cdb4-4251-a968-a0e0c1da9d4f" />

## Telegram Integration Module Aspect

To enhance real-time emergency intake, we developed a Telegram-based interface that allows users to report incidents using text, voice, and location sharing.

### Features

- Voice message input with automatic transcription
- AI-powered emergency classification
- GPS location integration
- Structured emergency report generation
- Human-in-the-loop verification (Confirm / Edit / Dispatch)

### Example Output
🚑 EMERGENCY REPORT

Incident Type: Fire
Injured: 9
Location: Near SIIT
Severity: High
Confidence: 0.85

### Workflow
```
User (Telegram)
   ↓
Voice / Text Input
   ↓
Speech-to-Text (if voice)
   ↓
AI Processing (LLM)
   ↓
Structured Emergency Report
   ↓
Operator Verification (Confirm / Edit)
   ↓
Dispatch
```

### Implementation

The Telegram bot is implemented using:

- `python-telegram-bot` for bot interaction
- OpenAI API for transcription and analysis
- Async event handling for real-time responsiveness

  
### Demo
<img width="956" height="862" alt="Screenshot 2569-03-28 at 15 03 31 1" src="https://github.com/user-attachments/assets/52812256-02e2-47b1-8b28-252be1c634be" />

