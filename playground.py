from security import create_access_token, decode_access_token
import jwt

print('Valid Token')

token = create_access_token(3, expires_in_minutes=-1)

print(token)

print('\nDecoded:')

try:
    print(decode_access_token(token))
except jwt.ExpiredSignatureError:
    print('token has expired') 
