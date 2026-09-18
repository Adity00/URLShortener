from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = "dev-secret-key-for-url-shortener-123456"
ph = PasswordHasher()

def hash_password(password):
    return ph.hash(password)

def verify_password(password, password_hash):
    try:
        return ph.verify(password_hash, password)
    except VerifyMismatchError:
        return False

def create_access_token(user_id, expires_in_minutes=30):
    expiration = datetime.now(timezone.utc)+timedelta(minutes=expires_in_minutes)
    payload = {
        'sub':str(user_id),
        'exp':expiration
    }

    token = jwt.encode(
        payload=payload,
        key=SECRET_KEY,
        algorithm='HS256'
    )

    return token

def decode_access_token(token):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=['HS256']
    )

    return payload
