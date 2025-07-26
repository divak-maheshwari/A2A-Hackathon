import os
import httpx

async def send_followup(to_email, status):
    # Could plug in Vapi or other sponsor APIs. Here, just log for demo.
    print(f"Pretend sent followup to {to_email}, Status: {status}")
    return True
