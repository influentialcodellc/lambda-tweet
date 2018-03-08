import base64
import logging
import os
import tweet
import boto3
import twitter


def decrypt_env_var(env_var: str) -> str:
    """
    example return value from `decrypt`
    {
    'KeyId': 'string',
    'Plaintext': b'bytes'
    }
    """
    return boto3.client('kms').decrypt(CiphertextBlob=base64.b64decode(env_var))['Plaintext'].decode('utf-8')


URL_BASE = os.environ['URL_BASE']
DECRYPTED_TOKEN = decrypt_env_var(os.environ['TOKEN'])
DECRYPTED_TOKEN_SECRET = decrypt_env_var(os.environ['TOKEN_SECRET'])
DECRYPTED_CONSUMER_KEY = decrypt_env_var(os.environ['CONSUMER_KEY'])
DECRYPTED_CONSUMER_SECRET = decrypt_env_var(os.environ['CONSUMER_SECRET'])


def lambda_handler(event, context):
    logger = logging.getLogger('tweet')
    logger.setLevel(logging.INFO)
    keys = [record['s3']['object']['key'] for record in event.get('Records', [])]
    if not keys or len(keys) > 1:
        logger.error('Only one new post at a time is expected.')
        return

    t = twitter.Twitter(auth=twitter.OAuth(token=DECRYPTED_TOKEN,
                                           token_secret=DECRYPTED_TOKEN_SECRET,
                                           consumer_key=DECRYPTED_CONSUMER_KEY,
                                           consumer_secret=DECRYPTED_CONSUMER_SECRET))
    tweeter = tweet.Tweeter(t)
    tweeter.tweet(f"{URL_BASE}/{keys[0]}")
