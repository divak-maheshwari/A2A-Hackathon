import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from resume_llm import screen_resume
from scheduler import schedule_interview
from followup import send_followup
from orchestrator import trigger_orkes_workflow
from datadog import initialize, api as datadog_api

# Datadog setup
DATADOG_API_KEY = "ef8e2d3af50803562bf01ec0998e04fd"
if DATADOG_API_KEY:
    initialize(api_key=DATADOG_API_KEY)

app = FastAPI()

# Allow CORS so React can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React's dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/hello")
def read_root():
    return {"message": "Hello from FastAPI!"}


# If in main.py, skip APIRouter - just use your app instance




@app.post("/api/upload_resume")
async def upload_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    # 1. Read and decode the uploaded resume
    contents = await file.read()
    try:
        resume_text = contents.decode("utf-8", errors="ignore")
    except Exception as e:
        return {"error": f"Could not decode file: {e}"}

    # 2. Call your provided screen_resume function (with Senso integration)
    try:
        parsed_data = await screen_resume(resume_text, job_description)
    except Exception as e:
        return {"error": f"Failed to screen resume: {e}"}

    # 3. Optionally: Datadog reporting
    if DATADOG_API_KEY and datadog_api:
        try:
            datadog_api.Event.create(
                title="Resume Uploaded",
                tags=["resume", "screening"]
            )
        except Exception as dd_err:
            print("[Datadog Error]", dd_err)

    # 4. Return all relevant info to the frontend
    return {
        "parsed": parsed_data
    }


@app.post("/schedule")
async def schedule(candidate_email: str = Form(...)):
    link = await schedule_interview(candidate_email)
    if DATADOG_API_KEY:
        datadog_api.Event.create(
            title="Interview Scheduled", text=f"Email: {candidate_email}", tags=["schedule"]
        )
    return {"link": link}

@app.post("/followup")
async def followup(candidate_email: str = Form(...), status: str = Form(...)):
    await send_followup(candidate_email, status)
    if DATADOG_API_KEY:
        datadog_api.Event.create(
            title="Followup Sent", text=f"Email: {candidate_email}, Status: {status}", tags=["followup"]
        )
    return {"ok": True}

@app.post("/orkes_orchestrate")
async def orkes_orchestrate(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    candidate_email: str = Form(...),
    status: str = Form(...)
):
    contents = await file.read()
    orchestration_result = await trigger_orkes_workflow(
        contents.decode(), job_description, candidate_email, status
    )
    return orchestration_result
