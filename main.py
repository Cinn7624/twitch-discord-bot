from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# Load your Discord webhook from environment variable
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.get("/")
def home():
    return {"status": "ok", "message": "Twitch-Discord bot is running!"}

@app.post("/twitch-command")
async def twitch_command(request: Request):
    try:
        data = await request.json()
        command = data.get("command")
        user = data.get("user")
        message = data.get("message", "")

        if not DISCORD_WEBHOOK_URL:
            return {"error": "Missing DISCORD_WEBHOOK_URL"}

        # Customize your Discord message format here
        payload = {
            "content": f"**{user}** ran {command} — {message}"
        }

        # Send to Discord
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

        if response.status_code == 204:
            return {"status": "success", "message": "Posted to Discord!"}
        else:
            return {"status": "error", "discord_response": response.text}
    except Exception as e:
        return {"status": "error", "details": str(e)}

if __name__ == "__main__":
    import uvicorn
    # Run the app on port 8080 (Koyeb will detect this automatically)
    uvicorn.run(app, host="0.0.0.0", port=8080)


