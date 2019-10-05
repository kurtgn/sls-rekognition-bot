import logging
import os

import boto3


logger = logging.getLogger(__name__)


client = boto3.client('lambda')


def upload_env_vars():
    logger.warning('Uploading Lambda config variables...')
    client.update_function_configuration(
        FunctionName=os.environ['LAMBDA_FUNCTION_NAME'],
        Environment={
            'Variables': {
                'TELEGRAM_TOKEN': os.environ['TELEGRAM_TOKEN'],
                'BUCKET_NAME': os.environ['BUCKET_NAME'],
                'DB_NAME': os.environ['DB_NAME'],
            }
        },
    )
