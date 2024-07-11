from fastapi import APIRouter, Depends,HTTPException
from database.db import get_db
from schema.loginschema import LoginDetailsResponse,LoginDetailsResponseData,Token
from sqlalchemy.orm import Session
from models.loginmodel import LoginDetails
from crud.logincrud import authenticate_user

router =  APIRouter()

@router.post('/tocken',response_model=Token)
async def login_for_access_tocken(login_req:LoginDetailsResponse, db:Session = Depends(get_db)):
    authenticate= authenticate_user(db, login_req.email_address, login_req.password)
    if not authenticate:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return authenticate

