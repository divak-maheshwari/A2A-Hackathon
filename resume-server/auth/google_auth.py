# auth/google_auth.py
from arcadepy import Arcade

client = Arcade()  # Loads ARCADE_API_KEY from env

async def authorize_google(user_id: str):
    auth_response = client.auth.start(
        user_id=user_id,
        provider="google",  # or your custom one like "google-auth-resume"
        scopes=["https://www.googleapis.com/auth/gmail.send"],
    )

    if auth_response.status != "completed":
        return {"auth_url": auth_response.url, "status": "pending"}

    final = client.auth.wait_for_completion(auth_response)
    token = final.context.token

    return {"token": token, "status": "completed"}
