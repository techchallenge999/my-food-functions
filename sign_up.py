import os

from passlib.context import CryptContext
import redis


def lambda_handler(event, context):
    body = event["body"]

    body["password"] = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(body["password"])

    redis_key = f'cpf:{body["cpf"]}'
    del body["cpf"]

    redis.Redis(host=os.environ["REDIS_URL"], port=6379, db=0).set(redis_key, body)

    return {"statusCode": 200}
