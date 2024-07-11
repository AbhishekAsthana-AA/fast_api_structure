from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginDetailsResponse(BaseModel):
    email_address:str
    password:str

class LoginDetailsResponseData(BaseModel):
    email_address:str
    employee_id:int