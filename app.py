from datetime import datetime

import requests
from flask import Flask, escape, request

import utils

app = Flask(__name__)


@app.route('/telegram_webhook', methods=['POST'])
def hello():
    body = request.json

    chat_id = body['message']['chat']['id']

    picture_url = utils.bot.fetch_image_from_tg_payload(payload=body)
    if not picture_url:
        utils.bot.send_text_message(
            chat_id=chat_id,
            text='This is not an image. I only work with images.',
        )
        return {'status': 'ok'}

    res = requests.get(picture_url)

    emotions = utils.get_emotions(res.content)

    if not emotions:
        utils.bot.send_text_message(
            chat_id=chat_id,
            text='Unable to detect emotions. This is probably not a face.',
        )

        return {'status': 'ok'}

    text = utils.emotions_summary(emotions)
    utils.bot.send_text_message(chat_id=chat_id, text=text)

    s3_url = utils.upload_to_s3(url=picture_url, content=res.content)

    first_emotion = emotions[0]
    selfie = utils.Selfie(
        emotion_type=first_emotion.type,
        emotion_confidence=first_emotion.confidence,
        timestamp=datetime.now(),
        url=s3_url,
    )
    utils.put_selfie(selfie)

    return {'status': 'ok'}


@app.cli.command("prepare")
def setup():
    utils.prepare_env()


@app.cli.command("createdb")
def setup():
    utils.create_table()
    utils.create_bucket()


@app.cli.command("connect-bot")
def post_setup():
    utils.upload_env_vars()
    utils.set_webhook()


@app.cli.command("dropdb")
def teardown():
    utils.delete_table()
    utils.delete_bucket()


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port='5000')
