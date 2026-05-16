import os

import requests
from dotenv import load_dotenv

from backend.prompts import CUSTOMER_SERVICE_SYSTEM_PROMPT


load_dotenv()


def get_customer_service_reply(user_message: str) -> str:
    """Call the configured LLM and return a customer-service reply."""
    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").rstrip("/")
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")

    if not api_key or api_key == "你的key":
        raise RuntimeError("请先在 .env 中配置真实的 DEEPSEEK_API_KEY")

    response = requests.post(
        f"{base_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": CUSTOMER_SERVICE_SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            "temperature": 0.3,
        },
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
