from fastapi import FastAPI, Request
import httpx
import os
from dotenv import load_dotenv

# Load environment variables (for your Discord webhook URL)
load_dotenv()
app = FastAPI()

# Get the Discord webhook URL from your environment variables
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# ✅ Combined GET + POST route for maximum compatibility
@app.api_route("/twitch-command", methods=["GET", "POST"])
async def twitch_command(request: Request):
    if request.method == "POST":
        # If Nightbot or other services can send JSON (POST)
        data = await request.json()
        command = data.get("command")
        user = data.get("user")
        message = data.get("message", "")
    else:
        # If Nightbot uses GET requests
        command = request.query_params.get("command")
        user = request.query_params.get("user")
        message = request.query_params.get("message", "")

    # Basic validation
    if not command or not user:
        return {"error": "Missing required fields"}

    # Format message for Discord
    if message:
        discord_message = f"🎥 **{user}** used `{command}`: {message}"
    else:
        discord_message = f"🎥 **{user}** used `{command}`"

    # Send to Discord
    async with httpx.AsyncClient() as client:
        await client.post(DISCORD_WEBHOOK_URL, json={"content": discord_message})

    return {"status": "ok", "sent": discord_message}


