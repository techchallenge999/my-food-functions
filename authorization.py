import json
import os

import redis


def lambda_handler(event, context):
    body = event["body"]

    encoded_jwt = body["token"]
    value = redis.Redis(host=os.environ["REDIS_URL"], port=6379, db=0).get(f"token:{encoded_jwt}")

    if not value:
        return {"statusCode": 401}

    value_dict = json.loads(value)
    value_dict["statusCode"] = 200
    return value_dict
