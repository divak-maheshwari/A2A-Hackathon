import os
import httpx

ORKES_API_KEY = os.getenv("ORKES_API_KEY")
ORKES_WORKFLOW_URL = os.getenv("ORKES_WORKFLOW_URL")

async def trigger_orkes_workflow(resume, job_description, candidate_email, status):
    # Orkes: fire workflow using API (pseudo, wraps all stages)
    if ORKES_API_KEY and ORKES_WORKFLOW_URL:
        payload = {
            "resume": resume,
            "job_description": job_description,
            "candidate_email": candidate_email,
            "status": status
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                ORKES_WORKFLOW_URL,
                json=payload,
                headers={"Authorization": f"Bearer {ORKES_API_KEY}"}
            )
            if resp.status_code == 200:
                return resp.json()
    # fallback: just echo for demo
    return {"msg": "Orkes step simulated (plug API for live workflow tracking)"}
