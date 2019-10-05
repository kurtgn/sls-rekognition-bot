from app import TG_TOKEN
from utils.telegram import set_webhook


set_webhook(
    # url='https://9qndtrt4q8.execute-api.us-east-1.amazonaws.com/dev/telegram_webhook',

    url='https://p6001.forwarding.fstrk.io/telegram_webhook',
    tg_token=TG_TOKEN
)

