import requests


class TelegramBot:
    old_id = 0

    def __init__(self, TOKEN: str):
        self.url_base = f"https://api.telegram.org/bot{TOKEN}"

    def get_updates(self) -> dict:
        url = self.url_base + "/getUpdates?offset=-1"
        try:
            with requests.get(url) as response:
                if response.status_code == 200:
                    data = response.json()
                    # Analysis Messages
                    try:
                        message_id = data["result"]
                        message_id = message_id[0]["message"]["message_id"]
                        if message_id == self.old_id:
                            return {}
                    except IndexError:
                        return {}

                    return data

        except requests.ConnectTimeout:
            return self.get_updates()

        return {}

    def send_message(self, chat_id: int, text: str, reply_message_id: int = 0) -> bool:
        url = self.url_base + "/sendMessage"
        req_data = {
            "chat_id": chat_id,
            "text": text,
            "reply_to_message_id": reply_message_id,
        }
        response = requests.post(url, data=req_data)
        if response.status_code == 200:
            self.old_id = reply_message_id
            response.close()

            return True

        return False
