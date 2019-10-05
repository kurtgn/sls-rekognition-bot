import os
from uuid import uuid4

import boto3
import requests

s3 = boto3.resource('s3')


BUCKET_NAME = 'serverless-rekognition-chatbot'


def create_bucket():
    bucket = s3.create_bucket(Bucket=BUCKET_NAME)
    print(bucket)


def delete_bucket():
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
