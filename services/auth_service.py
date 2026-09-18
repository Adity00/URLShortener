from database.queries import create_user, get_user_by_email
from security import hash_password, verify_password, create_access_token

def register_user(email, password):
    return create_user(email,hash_password(password))


def login_user(email, password):
    details = get_user_by_email(email)

    if details is None:
        return None

    if not verify_password(password, details['password_hash']):
        return None

    token = create_access_token(details['id'])

    return token
                                