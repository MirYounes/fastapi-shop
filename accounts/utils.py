from os import stat
from passlib.context import CryptContext
from fastapi_mail import FastMail, MessageSchema
import settings
import uuid
import redis


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



redis = redis.Redis(host='redis', port='6379')


def _generate_code():
    return uuid.uuid4().hex


class Hash():
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(password):
        return pwd_context.hash(password)



def add_to_redis(id, state):
    token = _generate_code()
    redis.set(name=f'{state}_{id}', value=token.encode('utf-8'), ex=3600)
    return token

def get_from_redis(id, state):
    token = redis.get(name=f'{state}_{id}').decode('utf-8')
    return token

def delete_from_redis(id, state):
    redis.delete(f'{state}_{id}')


def send_email_async(email, token, subject, background_tasks):
    message = MessageSchema(
        subject=subject,
        recipients=[email, ],
        body=''.join(token),
    )
    from main import conf
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)


def send_email(id,  email, state, subject, background_tasks):
    #print(id)
    #print(email)
    delete_from_redis(id=id, state=state)
    token = add_to_redis(id=id, state=state),
    send_email_async(email=email, token=token, subject=subject,
               background_tasks=background_tasks)
