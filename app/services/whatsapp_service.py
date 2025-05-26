import requests
import os
from app.core.config import settings

def send_whatsapp_message(phone: str, message: str) -> int:
    url = settings.WHATSAPP_API_URL
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": phone,
        "message": message
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code
