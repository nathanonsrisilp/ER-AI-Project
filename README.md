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
