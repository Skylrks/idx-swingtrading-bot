import os
import requests
from dotenv import load_dotenv

load_dotenv()

def kirim_pesan(pesan: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": pesan,
        "parse_mode": "HTML"
    }
    
    response = requests.post(url, json=payload)
    return response.json()

if __name__ == "__main__":
    hasil = kirim_pesan("🤖 IDX Trading Bot aktif! Sistem berjalan normal.")
    print(hasil)