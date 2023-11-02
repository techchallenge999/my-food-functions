import json
import os

import redis


def lambda_handler(event, context):
    value = redis.Redis(host=os.environ["REDIS_URL"], port=6379, db=0).get(f'token:{event["token"]}')

    if not value:
        return {"statusCode": 401}

    return json.loads(value)
