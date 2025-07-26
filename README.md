# A2A-Hackathon
Enterprise + Ambient Agents Hackathon

# Recruiter Assistant AI

Streamlines the entire hiring process by automating resume screening, candidate evaluation, interview scheduling, and follow-ups—all in one intelligent workflow. It helps recruiters save time, reduce manual effort, and focus on making better hiring decisions faster.

Built with **FastAPI** (Python) backend and **React** frontend, integrated with sponsor tools like Senso, Google DeepMind, Arcade, and Datadog 

---
## Features
- **Resume Screening:**  
  Upload resumes and job descriptions for AI-powered suitability scoring and structured candidate data extraction.

- **Candidate Scoring:**  
  Automatically generate interview scheduling links (stubbed or via Arcade API).

- **Email & Follow-Up:**  
  Send automated acceptance/rejection follow-up emails.

- **Interview Scheduling:**  
  Seamlessly books interview slots and sends invites. 
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


