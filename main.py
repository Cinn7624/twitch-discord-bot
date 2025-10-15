from fastapi import FastAPI, Request
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Get Discord webhook URL from environment variables
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# ✅ Combined GET + POST route for compatibility (Nightbot, etc.)
@app.api_route("/twitch-command", methods=["GET", "POST"])
async def twitch_command(request: Request):
    if request.method == "POST":
        data = await request.json()
        command = data.get("command")
        user = data.get("user")
        message = data.get("message", "")
    else:
        command = request.query_params.get("command")
        user = request.query_params.get("user")
        message = request.query_params.get("message", "")

    # Validation
    if not command or not user:
        return {"error": "Missing required fields"}

    # Format message for Discord
    if message:
        discord_message = f"🎥 **{user}** used `{command}`: {message}"
    else:
        discord_message = f"🎥 **{user}** used `{command}`"

    # Send message to Discord
    async with httpx.AsyncClient() as client:
        await client.post(DISCORD_WEBHOOK_URL, json={"content": discord_message})

    # ✅ Clean Nightbot-friendly response
    return "✅ Message sent to Discord!"

