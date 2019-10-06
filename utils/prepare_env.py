import json
from pathlib import Path
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)

def prepare_env():
    """
    Add two lines to .env file:

    DBNAME=......
    BUCKET_NAME=.....

    also, add "s3_bucket" setting to zappa_settings.json
    """

    logger.warning('Updating .env and zappa_settings.json...')

    basedir = Path(__file__).parent.parent
    env_file = basedir / '.env'

    if env_file.exists():
        with env_file.open() as f:
            content = f.read()
    else:
        content = ''

    resourse_name = 'selfies-' + str(uuid4())[:8]

    if 'DB_NAME' not in content:
        content += f'\nDB_NAME={resourse_name}'
    if 'BUCKET_NAME' not in content:
        content += f'\nBUCKET_NAME={resourse_name}'

    with env_file.open('w') as f:
        f.write(content)

    zappa_settings = basedir / 'zappa_settings.json'
    with zappa_settings.open() as f:
        settings = json.load(f)

    if 's3_bucket' not in settings['dev']:
        settings['dev']['s3_bucket'] = resourse_name
        with zappa_settings.open('w') as f:
            f.write(json.dumps(settings, indent=4))



