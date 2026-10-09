import requests
import time
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_alert(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram not configured")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print("Failed to send Telegram alert:", e)


def get_updates(offset=None):
    """Get new messages from Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    params = {"timeout": 30, "offset": offset}
    try:
        response = requests.get(url, params=params, timeout=35)
        return response.json()
    except Exception as e:
        print("Error getting updates:", e)
        return None


def wait_for_new_task():
    """Watcher: waits until user sends a new task on Telegram"""
    print("\n😴 Watcher is sleeping... Send a new task on Telegram to wake me up.")
    send_alert("😴 Agents are sleeping.\nSend me a new task to wake them up.")

    offset = None
    while True:
        data = get_updates(offset)
        if data and data.get("ok") and data.get("result"):
            for update in data["result"]:
                offset = update["update_id"] + 1
                message = update.get("message", {})
                text = message.get("text", "").strip()
                chat_id = str(message.get("chat", {}).get("id", ""))

                if chat_id == str(TELEGRAM_CHAT_ID) and text:
                    print(f"\n🔔 New task received: {text}")
                    send_alert(f"🚀 Starting new task:\n{text}")
                    return text

        time.sleep(1)