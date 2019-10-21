import os
from datetime import datetime

import requests
from flask import Flask, request, render_template, url_for

import utils
from utils import get_selfies
from utils.rekognition import EmotionTypes, Emotion

app = Flask(__name__)


def get_position_in_top(emotion: Emotion):
    """
    Given an emotion, get its position in all of all emotions of this type
    """
    selfies = get_selfies(
        emotion_type=emotion.type, date=datetime.now(), limit=100
    )
    confidence_numbers = [s.emotion_confidence for s in selfies] + [
        emotion.confidence
    ]

    return (
        sorted(confidence_numbers, reverse=True).index(emotion.confidence) + 1
    )


def get_link_for_top_emotion(emotion_type: str, host: str) -> str:
    link = (
        host.rstrip('/')
        + url_for('top_for_emotion')
        + '?emotion='
        + emotion_type
    )
    return link


@app.route('/top/')
def top_for_emotion():
    """ Render selfies with particular emotion """

    emotion = request.args.get('emotion', EmotionTypes.HAPPY)

    selfies = get_selfies(emotion_type=emotion, date=datetime.now(), limit=100)

    return render_template(
        'top_for_emotion.html',
        selfies=selfies,
        emotion=emotion,
        EmotionTypes=EmotionTypes,
    )


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

    top_emotion = emotions[0]

    position = get_position_in_top(emotion=top_emotion)

    text = utils.emotions_summary(emotions)
    link = get_link_for_top_emotion(top_emotion.type, host=request.host_url)
    text += (
        f'\n\n👌 You are *#{position} {top_emotion.type} person* today!'
        f'\nView all {top_emotion.type} people: {link}'
    )
    utils.bot.send_text_message(chat_id=chat_id, text=text)

    s3_url = utils.upload_to_s3(url=picture_url, content=res.content)

    selfie = utils.Selfie(
        emotion_type=top_emotion.type,
        emotion_confidence=top_emotion.confidence,
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')
