from operator import itemgetter
from typing import Optional

import requests


class Bot:
    """
    simple implementation of needed Telegram functions.
    We don't need any libraries for that
    """

    BASE_URL = 'https://api.telegram.org/bot'

    def __init__(self, token):
        self.token = token

    def set_webhook(self, url: str) -> None:
        response = requests.post(
            f'https://api.telegram.org/bot{self.token}/setWebhook',
            json={'url': url},
        )
        print(response.json())

    def fetch_image_from_tg_payload(self, payload: dict) -> Optional[str]:
        if 'photo' not in payload['message']:
            return None

        pictures = payload['message']['photo']

        pictures = sorted(pictures, key=itemgetter('file_size'))
        picture = pictures[-1]

        file_path = requests.post(
            f'https://api.telegram.org/bot{self.token}/getFile',
            json={'file_id': picture['file_id']},
        ).json()['result']['file_path']

        url = f'https://api.telegram.org/file/bot{self.token}/{file_path}'

        return url

    def send_text_message(self, chat_id: int, text: str) -> None:

        requests.post(
            f'https://api.telegram.org/bot{self.token}/sendMessage',
            json={'chat_id': chat_id, 'text': text},
        )
