# Geospatial AI Document Orchestrator 🌍

### Project Overview
An automated pipeline that extracts critical site safety data from geospatial reports. Using **Google Gemma**, the system identifies flood and seismic risks. If a "High" risk is detected, a secondary AI agent drafts a professional alert and sends it via **n8n automation**.

### Tech Stack
* **Frontend:** Streamlit
* **AI Model:** Google Gemma (via Google AI Studio)
* **Automation:** n8n (Webhooks, Gmail API, AI Agents)
* **Language:** Python

### How it Works
1. **Upload:** User uploads a geospatial report to the Streamlit UI.
2. **Analysis:** Gemma extracts GPS coordinates and assesses risk levels.
3. **Orchestration:** A webhook triggers an n8n workflow.
4. **Action:** If risk is High, a Project Manager receives an automated email alert with a mitigation plan.

### Repository Contents
* `app.py`: The main Streamlit application.
* `n8n_workflow.json`: The exported n8n workflow logic.
* `requirements.txt`: Python dependencies.
