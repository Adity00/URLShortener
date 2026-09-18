from pydantic import BaseModel, HttpUrl, Field, EmailStr
from datetime import datetime
class URLRequest(BaseModel):
    url : HttpUrl
    expires_in: int | None = Field(default=None, gt=0)

class URLResponse(BaseModel):
    original_url:HttpUrl
    shortcode:str
    expires_at:datetime | None = None

class URLStatsResponse(BaseModel):
    shortcode:str
    original_url:HttpUrl
    clicks:int
    expires_at:datetime | None = None    

class RegisterRequest(BaseModel):
    email:EmailStr
    password:str

class LoginRequest(BaseModel):
    email:EmailStr
    password:str
    