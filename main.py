from fastapi import FastAPI, Request
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.post("/twitch-command")
async def twitch_command(request: Request):
    data = await request.json()
    command = data.get("command")
    user = data.get("user")

    message = f"Twitch user **{user}** ran the command: `{command}`"

    async with httpx.AsyncClient() as client:
        await client.post(DISCORD_WEBHOOK_URL, json={"content": message})

    return {"status": "sent to discord"}

from fastapi import Request
from fastapi.responses import JSONResponse

@app.get("/twitch-command")
async def twitch_command_get(command: str, user: str, message: str = ""):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if message:
        content = f"🎬 Twitch user **{user}** ran `{command}`: {message}"
    else:
        content = f"🎬 Twitch user **{user}** ran `{command}`"

    async with httpx.AsyncClient() as client:
        await client.post(webhook_url, json={"content": content})
    return {"status": "sent to discord"}

