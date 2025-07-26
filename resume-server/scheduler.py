import datetime
import os
import httpx

ARCADE_API_KEY = os.getenv("ARCADE_API_KEY")

async def schedule_interview(candidate_email):
    # Arcade: Tool-calling scheduling (pseudo, replace with real integration)
    if ARCADE_API_KEY:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.arcade-ai.com/v1/schedule",
                json={"email": candidate_email},
                headers={"Authorization": f"Bearer {ARCADE_API_KEY}"}
            )
            if resp.status_code == 200:
                return resp.json().get("link")
    # fallback: mock
    d = datetime.date.today() + datetime.timedelta(days=3)
    return f"https://calendly.com/demo/interview?email={candidate_email}&date={d}"
