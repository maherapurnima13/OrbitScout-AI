import httpx
import os
from dotenv import load_dotenv

load_dotenv()

TINYFISH_API_KEY = os.getenv("TINYFISH_API_KEY")

TINYFISH_ENDPOINT = "https://agent.tinyfish.ai/v1/automation/run-sse"


async def run_tinyfish_agent(task):

    payload = {
        "task": task,
        "mode": "browser",
        "max_steps": 10
    }

    headers = {
        "Authorization": f"Bearer {TINYFISH_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=60) as client:

        response = await client.post(
            TINYFISH_ENDPOINT,
            json=payload,
            headers=headers
        )

        return response.json()