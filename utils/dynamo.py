import logging
import os
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from operator import attrgetter
from typing import List

import boto3
from boto3.dynamodb.conditions import Key
from dateutil.parser import parse

logger = logging.getLogger(__name__)

dynamodb = boto3.resource('dynamodb')


DB_NAME = os.environ.get('DB_NAME')


def create_table():
    logger.warning(f'creating table {DB_NAME}...')

    dynamodb.create_table(
        AttributeDefinitions=[
            {'AttributeName': 'emotion_type', 'AttributeType': 'S'},
            {'AttributeName': 'timestamp', 'AttributeType': 'S'},
            # {'AttributeName': 'emotion_confidence', 'AttributeType': 'N'},
        ],
        TableName=DB_NAME,
        KeySchema=[
            {'AttributeName': 'emotion_type', 'KeyType': 'HASH'},
            {'AttributeName': 'timestamp', 'KeyType': 'RANGE'},
        ],
        BillingMode='PAY_PER_REQUEST',
    )


def delete_table():
    logger.warning(f'deleting table {DB_NAME}...')
    table = dynamodb.Table(DB_NAME)
    table.delete()


@dataclass
class Selfie:
    emotion_type: str
    emotion_confidence: float
    url: str
    timestamp: datetime


def put_selfie(selfie: Selfie) -> None:
    table = dynamodb.Table(DB_NAME)
    table.put_item(
        Item={
            'emotion_type': selfie.emotion_type,
            'emotion_confidence': Decimal(str(selfie.emotion_confidence)),
            'url': selfie.url,
            'timestamp': selfie.timestamp.isoformat(),
        }
    )


def item_to_selfie(item: dict) -> Selfie:

    return Selfie(
        emotion_type=item['emotion_type'],
        emotion_confidence=float(item['emotion_confidence']),
        url=item['url'],
        timestamp=parse(item['timestamp']),
    )


def get_selfies(emotion_type: str, limit: int, date: datetime) -> List[Selfie]:
    """
    Get selfies for a particular emotion & date.

    Date is stored as string in ISO format. Querying by date is done like so:
        "get all items where timestamp begins with YYYY-MM-DD"

    """

    table = dynamodb.Table(DB_NAME)

    date_str = date.isoformat()[:10]  # YYYY-MM-DD

    response = table.query(
        KeyConditionExpression=Key('emotion_type').eq(emotion_type)
        & Key('timestamp').begins_with(date_str),
        ScanIndexForward=False,
        Limit=limit,
        ReturnConsumedCapacity='TOTAL',
    )

    # show how much money we're spending
    logger.warning(response['ConsumedCapacity'])

    items = response['Items']

    selfies = [item_to_selfie(item) for item in items]

    selfies = sorted(
        selfies, key=attrgetter('emotion_confidence'), reverse=True
    )

    return selfies


if __name__ == '__main__':

    # create_table()

    #
    # put_selfie(Selfie(
    #     emotion_type='bbb',
    #     emotion_confidence=12345.123321235,
    #     url='xxxx',
    #     timestamp=datetime.now()
    # ))

    results = get_selfies(emotion_type='HAPPY', date=datetime.now(), limit=100)
    for r in results:
        print(r)
