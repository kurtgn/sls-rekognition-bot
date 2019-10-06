import logging
import os
from uuid import uuid4

import boto3
import requests

logger = logging.getLogger(__name__)
s3 = boto3.resource('s3')


BUCKET_NAME = os.environ.get('BUCKET_NAME')


def create_bucket():
    logger.warning(f'creating bucket {BUCKET_NAME}...')
    s3.create_bucket(Bucket=BUCKET_NAME)


def delete_bucket():
    logger.warning(f'deleting bucket {BUCKET_NAME}...')
    bucket = s3.Bucket(BUCKET_NAME)
    bucket.objects.all().delete()
    bucket.delete()


def upload_to_s3(url: str, content: bytes) -> str:
    bucket = s3.Bucket(BUCKET_NAME)
    _, ext = os.path.splitext(url)
    key = str(uuid4()) + ext
    res = requests.get(url)
    bucket.put_object(Body=res.content, ACL='public-read', Key=key)
    url = f'https://{BUCKET_NAME}.s3.amazonaws.com/{key}'

    return url


if __name__ == '__main__':
    create_bucket()
    # print(upload_to_s3(
    #     'https://timesofindia.indiatimes.com/thumb/msid-67586673,width-800,height-600,resizemode-4/67586673.jpg'
    # ))
