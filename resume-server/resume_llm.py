import os
import httpx
import asyncio

SENSO_API_KEY = "tgr_t07YcHi6KH1UI-9_LDbUvM3QazJgHcscl-VudB-20VY"  # or use os.getenv(...)
SENSO_API = "https://sdk.senso.ai/api/v1"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LLAMAINDEX_API_KEY = os.getenv("LLAMAINDEX_API_KEY")

async def upload_resume_to_senso(resume: str):
    print("UPLOAD TO SENSO, resume length:", len(resume)) # Debu
    print("UPLOAD TO SENSO, resume contents:\n", repr(resume))
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SENSO_API}/content/raw",
            headers={
                "X-API-Key": SENSO_API_KEY,     # DO NOT use Bearer, just the key
                "Content-Type": "application/json"
            },
            json={
                "title": "Resume.txt",
                "text": resume                  # FIXED: key "text" not "body"
            }
        )
        print("SENSO UPLOAD RESP STATUS:", response.status_code)
        print("SENSO UPLOAD RESP BODY:", response.text)
        return response


async def wait_for_senso_completion(content_id, senso_api_key, max_tries=20, delay=2):
    url = f"{SENSO_API}/content/{content_id}"
    headers = {"X-API-Key": senso_api_key}
    for attempt in range(max_tries):
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
            try:
                data = resp.json()
            except Exception:
                data = {}
            status = data.get("processing_status")
            print(f"SENSO STATUS POLL (try {attempt+1}):", status)
            if status == "completed":
                return True
            elif status == "failed":
                raise RuntimeError(f"Senso processing failed: {data}")
        await asyncio.sleep(delay)
    raise TimeoutError("Senso processing not completed after polling.")

async def get_senso_skills(content_id: str):
    """Use Senso to extract a comma-separated list of technical and soft skills from the resume."""
    await wait_for_senso_completion(content_id, SENSO_API_KEY)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SENSO_API}/generate",
            headers={
                "X-API-Key": SENSO_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "instructions": "list all the skills required in tech industry from resume.",
                "filter": {"content_ids": [content_id]},
                "content_type": "extraction"
            }
        )
        print("SENSO GENERATE (SKILLS) RESP STATUS:", response.status_code)
        print("SENSO GENERATE (SKILLS) RESP BODY:", response.text)
        try:
            return response.json()
        except Exception:
            return {"error": response.text, "status_code": response.status_code}



async def get_senso_email_reply(content_id: str):
    """Use Senso to draft a good match email to the applicant."""
    await wait_for_senso_completion(content_id, SENSO_API_KEY)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SENSO_API}/generate",
            headers={
                "X-API-Key": SENSO_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "instructions": "Write a professional email to the applicant congratulating them that they are a strong match and inviting them to the next step. Use a friendly, encouraging tone.",
                "filter": {"content_ids": [content_id]},
                "content_type": "reply"
            }
        )
        print("SENSO GENERATE (EMAIL REPLY) RESP STATUS:", response.status_code)
        print("SENSO GENERATE (EMAIL REPLY) RESP BODY:", response.text)
        try:
            return response.json()
        except Exception:
            return {"error": response.text, "status_code": response.status_code}


async def get_senso_summary(content_id: str):
    # Wait for Senso to process the upload before generating
    await wait_for_senso_completion(content_id, SENSO_API_KEY)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SENSO_API}/generate",
            headers={
                "X-API-Key": SENSO_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "instructions": "tell me about the person", 
                "filter": {"content_ids": [content_id]},
                "content_type": "summary"
            }
        )
        print("SENSO GENERATE RESP STATUS:", response.status_code)
        print("SENSO GENERATE RESP BODY:", response.text)
        try:
            return response.json()
        except Exception:
            return {"error": response.text, "status_code": response.status_code}

async def screen_resume(resume, job_decription):
    senso_result = {}
    summary = ""
    skills = ""
    email_reply = ""
    if SENSO_API_KEY:
        upload_resp = await upload_resume_to_senso(resume)
        try:
            up_json = upload_resp.json()
        except Exception:
            up_json = {}
        # Use "id" (not "content_id") for content_id
        if upload_resp.status_code in (200, 201, 202) and "id" in up_json:
            content_id = up_json["id"]
            print("SENSO upload id:", content_id)

            # Call for summary
            gen_json_summary = await get_senso_summary(content_id)
            summary = gen_json_summary.get("generated_text", "")

            # Call for skills extraction
            gen_json_skills = await get_senso_skills(content_id)
            skills = gen_json_skills.get("generated_text", "")

            # Call for email reply
            gen_json_email = await get_senso_email_reply(content_id)
            email_reply = gen_json_email.get("generated_text", "")

            senso_result = {
                "content_id": content_id,
                "summary": summary,
                "skills": skills,
                "email_reply": email_reply,
                "generate_summary_error": gen_json_summary.get("error") if "error" in gen_json_summary else None,
                "generate_skills_error":  gen_json_skills.get("error") if "error" in gen_json_skills   else None,
                "generate_email_error":   gen_json_email.get("error") if "error" in gen_json_email     else None,
            }
        else:
            print("SENSO upload:", upload_resp.text)
            senso_result = {"upload_error": upload_resp.text}
    else:
        senso_result = {"error": "SENSO_API_KEY not set"}

    return senso_result




    
    # # --- LlamaIndex: AI Extraction ---
    # # (pseudocode -- in real, run as a microservice or use their SDK)
    # candidate_fields = {}
    # if LLAMAINDEX_API_KEY:
    #     # Assume LlamaIndex extracts structured candidate fields
    #     candidate_fields = {
    #         "name": "Jane Candidate",
    #         "skills": ["python", "fastapi", "ml"]
    #     }
    #     parsed["llamaindex"] = candidate_fields

    # # --- Google Gemini: Advanced AI Screening ---
    # screening = ""
    # score = 0
    # if GEMINI_API_KEY:
    #     async with httpx.AsyncClient() as client:
    #         prompt = f"Given the resume: {resume}\nAnd this job description: {job_description}\nScore their match (0-100) and say why."
    #         resp = await client.post(
    #             f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}",
    #             json={"contents": [{"role":"user","parts":[{"text": prompt}]}]}
    #         )
    #         if resp.status_code == 200:
    #             out = resp.json()
    #             screening = out.get("candidates", [{}])[0].get("content", "")
    #             # Extract score from content (demo logic)
    #             import re
    #             m = re.search(r'(\d{1,3})', screening)
    #             score = int(m.group(1)) if m else 50
    # else:
    #     # fallback: keyword match
    #     keywords = [kw.lower() for kw in job_description.split() if len(kw) > 3]
    #     score = int(100 * sum(kw in resume.lower() for kw in keywords) / len(keywords)) if keywords else 50
    #     screening = "Keywords matched: " + ", ".join([kw for kw in keywords if kw in resume.lower()])

    # return screening, score, parsed



