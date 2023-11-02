import json
import os

from passlib.context import CryptContext
import redis


def lambda_handler(event, context):
    event["password"] = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto").hash(event["password"])

    redis_key = f'cpf:{event["cpf"]}'
    del event["cpf"]

    redis.Redis(host=os.environ["REDIS_URL"], port=6379, db=0).set(redis_key, json.dumps(event))

    return {"statusCode": 200}
