# A2A---Hackathon
Enterprise + Ambient Agents Hackathon

# Recruitment Workflow Orchestrator

An end-to-end demo MVP that automates recruitment workflows — from AI-powered resume screening, to automated interview scheduling, to candidate follow-ups.  

Built with **FastAPI** (Python) backend and **React** frontend, integrated with sponsor tools like HockeyStack, Orkes, Senso, Google DeepMind Gemini, LlamaIndex, Arcade, AI Dungeon, and Datadog 
for a powerful hackathon-ready presentation.

---
## Features

- **Resume Screening:**  
  Upload resumes and job descriptions for AI-powered suitability scoring and structured candidate data extraction (leveraging Senso, LlamaIndex, Google DeepMind Gemini).

- **Interview Scheduling:**  
  Automatically generate interview scheduling links (stubbed or via Arcade API).

- **Candidate Follow-up:**  
  Send automated acceptance/rejection follow-up emails.

- **Sponsor Integrations:**  
  - **HockeyStack:** Frontend user journey analytics and event tracking  
  - **Orkes Conductor:** Backend workflow orchestration via API  
  - **Senso & LlamaIndex:** AI document processing and data extraction  
  - **Google DeepMind Gemini:** Advanced AI matching and scoring  
  - **Arcade:** Scheduling tool API integration (stub)  
  - **AI Dungeon:** Optional gamified candidate interview experience  
  - **Datadog:** Backend monitoring and event logging  
---

## Project Structure

<pre>
recruit-orchestrator/
├── backend/
│   ├── main.py                  # FastAPI application and API endpoints
│   ├── resume_llm.py            # AI-powered resume screening & sponsor integrations
│   ├── scheduler.py             # Interview scheduling API logic
│   ├── followup.py              # Candidate follow-up email logic
│   ├── orchestrator.py          # Orkes workflow orchestration integration
│   ├── requirements.txt         # Python dependencies
│   └── .env.example             # Example environment variable file
├── frontend/
│   ├── public/
│   │   └── index.html           # HTML file with HockeyStack analytics snippet
│   ├── src/
│   │   ├── App.js               # Main React application layout
│   │   ├── ResumeScreening.js   # React component for resume upload & AI screening
│   │   ├── Scheduler.js         # React component for interview scheduling
│   │   └── Followup.js          # React component for candidate follow-up
│   └── package.json             # Frontend dependencies and scripts
</pre>

## Getting Started

### Backend Setup

1. Navigate to the `backend` directory.

2. Copy `.env.example` to `.env` and add your actual API keys:
