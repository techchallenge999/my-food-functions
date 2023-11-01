from datetime import datetime, timedelta
import json
import os

from jose import jwt
from passlib.context import CryptContext
import redis


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ACCESS_TOKEN_EXPIRE_SECONDS = 60 * ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM = "HS256"
JWT_SECRET = "JWT_SECRET"


def lambda_handler(event, context):
    body = event["body"]

    if not body:
        value_dict = {"is_admin": False, "uuid": None}
    else:
        cpf = body["cpf"]
        value = redis.Redis(host=os.environ["REDIS_URL"], port=6379, db=0).get(f"cpf:{cpf}")

        if not (value and PWD_CONTEXT.verify(body["password"], (value_dict := json.loads(value))["password"])):
            return {"statusCode": 401}

        del value_dict["password"]

    encoded_jwt = generate_token()
    redis.Redis(host=os.environ["REDIS_URL"], port=6379, db=0).set(f"token:{encoded_jwt}", json.dumps(value_dict), ex=ACCESS_TOKEN_EXPIRE_SECONDS)
    return {"statusCode": 200, "token": encoded_jwt}


def generate_token() -> str:
    created_at = datetime.utcnow()
    expire = created_at + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt
