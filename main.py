from fastapi import FastAPI, Request
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.post("/twitch-command")
async def twitch_command(data: dict):
    print("Incoming data:", data)
    command = data.get("command")
    user = data.get("user")
    message = data.get("message", "")

    if message:
        discord_message = f"🎥 **{user}** used `{command}`: {message}"
    else:
        discord_message = f"🎥 **{user}** used `{command}`"

    async with httpx.AsyncClient() as client:
        await client.post(DISCORD_WEBHOOK_URL, json={"content": discord_message})

    return {"status": "ok", "sent": discord_message}


