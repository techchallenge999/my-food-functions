import json
import os

from passlib.context import CryptContext
import redis


def lambda_handler(event, context):
    if not (event and event.get("cpf") and event.get("password")):
        return {"statusCode": 400}

    redis_key = f'cpf:{event["cpf"]}'

    if redis.Redis(host=os.environ["REDIS_URL"], port=6379, db=0).get(redis_key):
        return {"statusCode": 401}

    del event["cpf"]
    event["password"] = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto").hash(event["password"])

    redis.Redis(host=os.environ["REDIS_URL"], port=6379, db=0).set(redis_key, json.dumps(event))

    return {"statusCode": 200}
