# ER-Helper: AI-Powered Emergency Dispatch Assistant

## Team Members
- **Member #1:** Celine Helene Margrethe Amandine Johnsen  
- **Member #2:** Nathanon Srisilp  
- **Member #3:** Nutt Sittichaiopas  
- **Member #4:** Wasin Promjun  
- **Member #5:** Siranut Usawasutsakorn  

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


**Computer Version (Operator Interface)**  
This interface represents the call center or operator-side system. It is used to review incoming emergency reports, verify AI-generated information, and manage the dispatch process. Operators can confirm, edit, or initiate response actions based on the structured data.

![2569-03-28 20 18 51](https://github.com/user-attachments/assets/e1679876-8dc0-4af5-b82c-c79976517ae1)
![2569-03-28 20 18 35](https://github.com/user-attachments/assets/579de3fa-0eff-4c20-bf04-943b877d1fc0)

**Mobile Version (User Interface via Telegram)**  
This interface allows users to report emergencies directly from their mobile devices. Users can send text messages, voice notes, or share their location. The system automatically processes the input, transcribes voice messages, and generates a structured emergency report in real time.

## IoT Integration (ESP32 Alert System)

In addition to the AI-based emergency intake system, an IoT component was implemented using an ESP32 microcontroller.

### Concept

The ESP32 acts as a real-time alert device that responds to incoming emergency events processed by the system.

- When a new emergency report is generated and confirmed:
  - A signal is sent to the ESP32
  - The ESP32 triggers a visual alert (LED ON/OFF)

### Purpose

This demonstrates how digital emergency data can be translated into physical actions, enabling:

- Real-time alert systems in control rooms  
- Visual emergency indicators  
- Integration with hardware-based response systems  

### System Flow Extension
```
Telegram User
↓
AI Processing (Transcription + Classification)
↓
Emergency Report Generated
↓
Dispatch Signal
↓
ESP32 Trigger
↓
LED Alert (ON/OFF)
```

### Technologies Used

- ESP32 Microcontroller  
- Arduino Framework  
- Serial / API communication with backend

- ## AI Processing Concept

The system uses AI to transform unstructured user input into structured emergency data.

### 1. Voice-to-Text (Speech Recognition)

- Voice messages from Telegram are converted into text using AI transcription
- This enables hands-free emergency reporting

### 2. Natural Language Processing (LLM)

The transcribed or typed input is analyzed using a Large Language Model (LLM) to extract:

- Incident Type (e.g., fire, accident)
- Number of injured
- Location
- Severity level
- Confidence score

### 3. Structured Output

The system converts natural language into a standardized emergency report format:
Incident Type: Fire
Injured: 9
Location: Near SIIT
Severity: High
Confidence: 0.85
### 4. Human-in-the-Loop Verification

Before dispatch:

- The operator reviews the AI-generated report
- Can confirm, edit, or trigger dispatch

This ensures both automation and reliability.

## AI Engineering Approach

Beyond basic AI usage, this project focuses on the engineering of how AI is applied within a real-world system.

### 1. Prompt Engineering

The system is designed using structured prompts to guide the AI model in extracting relevant emergency information.

- Inputs are formatted to highlight key details (incident, location, severity)
- Prompts are optimized to produce consistent and structured outputs
- The AI is guided to return standardized fields instead of free-form text

### 2. Category & Format Engineering

To ensure reliability, the system enforces predefined categories and output formats:

- Incident Types (e.g., Fire, Accident, Medical Emergency)
- Severity Levels (Low, Medium, High)
- Structured response templates for consistency

This reduces ambiguity and improves downstream processing (e.g., dispatch decisions).

### 3. AI-Assisted Idea Generation

AI is also used as a support tool during development:

- Suggesting improvements to system design
- Assisting in defining workflows and architecture
- Helping refine emergency classification logic

### 4. Iterative Improvement

The system is designed to be continuously improved:

- Reviewing outputs to refine prompts
- Adjusting extraction logic based on real examples
- Enhancing accuracy and confidence scoring over time

This reflects an engineering approach where AI is not static, but optimized through iteration.

### 5. Human + AI Collaboration

Rather than replacing human decision-making, the system integrates:

- AI for speed and automation  
- Human operators for validation and control  

This hybrid approach ensures both efficiency and reliability in emergency scenarios.
