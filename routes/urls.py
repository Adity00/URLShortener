from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import RedirectResponse

from models.url import URLRequest,URLResponse,URLStatsResponse,RegisterRequest, LoginRequest
from services.url_service import create_short_url, get_url_for_redirect, get_stats_for_url
from exceptions import URLCreationError,URLExpiredError,URLNotFoundError
from services.auth_service import register_user, login_user
from dependancies import get_current_user


router = APIRouter()


@router.post("/shorten",response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def shorten(request: URLRequest,
            user_id:int = Depends(get_current_user)
            ):
    try:
        short_code, expires_at = create_short_url(
            request.url,
            user_id,
            request.expires_in
        )

    except URLCreationError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='could not create short URL'
        )    

    return {
        "original_url": request.url,
        "shortcode": short_code,
        "expires_at":expires_at
    }


@router.get("/stats/{code}", response_model=URLStatsResponse)
def stats(code: str, user_id:int = Depends(get_current_user)):
    try:
        record = get_stats_for_url(code, user_id)
        
    except URLNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short code not found"
        )

    return {
        'shortcode':code,
        'original_url':record['url'],
        'clicks':record['clicks'],
        'expires_at':record['expires_at']
    }    

    
@router.get('/me')
def me(user_id: int = Depends(get_current_user)):
    return{
        'user_id':user_id
    }


@router.get("/{code}")
def redirect_url(code: str):
    try:
        result = get_url_for_redirect(code)

    except URLExpiredError:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail='URL_Expired'
        )

    except URLNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Short code not found'
        )

    return RedirectResponse(
        url=result['url'],
        status_code=302
    )


@router.post('/register')
def register(request: RegisterRequest):
    result = register_user(
        request.email,
        request.password
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email Already registerd"
        )

    else:
        return{
            'message':'User registered'
        }


@router.post('/login')
def login(request:LoginRequest):
    token = login_user(request.email, request.password)

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Email or Password'
        )

    return{
        'access_token':token,
        'token_type':'bearer'
    }
