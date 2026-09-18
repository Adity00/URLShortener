from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')  #tokenUrl='/login' just for docu purposes

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)

        user_id = payload.get('sub')

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid Auth Credentials'
            )
        return int(user_id)

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid auth Credentials'
        )
    