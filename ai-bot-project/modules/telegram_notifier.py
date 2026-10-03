import os
import requests


class TelegramNotifier:
    """Sends signal alerts to Telegram. Credentials come from environment variables
    TELEGRAM_TOKEN and CHAT_ID (never commit them to the repository)."""

    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("CHAT_ID")

    @property
    def enabled(self):
        return bool(self.token and self.chat_id)

    def send_alert(self, message, image_path=None):
        if not self.enabled:
            print("Telegram not configured (set TELEGRAM_TOKEN and CHAT_ID); skipping alert.")
            return
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        requests.post(url, data={"chat_id": self.chat_id, "text": message, "parse_mode": "HTML"}, timeout=15)
        if image_path:
            self.send_photo(image_path, message)

    def send_photo(self, image_path, caption=""):
        url = f"https://api.telegram.org/bot{self.token}/sendPhoto"
        with open(image_path, "rb") as photo:
            requests.post(url, files={"photo": photo}, data={"chat_id": self.chat_id, "caption": caption}, timeout=30)
