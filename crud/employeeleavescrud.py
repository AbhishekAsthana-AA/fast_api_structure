from tkinter import NO
from fastapi import Depends, HTTPException,status
from sqlalchemy.orm import Session
from models.employee_modal import employeeLeaveDetails
from models.employee_login_models import employeeLoginDetails
from models.loginmodel import LoginDetails,UserDetails
# from models import EmployeeLeaveDetails, EmployeeLoginDetails
from sqlalchemy import or_, and_
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List

def serialize_model(model_instance):
    """Convert SQLAlchemy model instance to dictionary."""
    return {column.name: getattr(model_instance, column.name) for column in model_instance.__table__.columns}

def getEmployeeLeaves(db:Session, payload:list):
    query = db.query(employeeLeaveDetails)
    if payload.start_date and payload.end_date:
        query = query.filter(
        or_(
            and_(
                employeeLeaveDetails.start_date <= payload.start_date,
                employeeLeaveDetails.end_date >= payload.end_date
            ),
            and_(
                employeeLeaveDetails.start_date <= payload.end_date,
                employeeLeaveDetails.end_date >= payload.start_date
            )
        )
     )
    else:
      query = query
    # print(query.statement)
    # compiled_query = query.statement.compile(compile_kwargs={"literal_binds": True})
    # print(compiled_query)
    result = query.all()
    return result

def insertEmpDetails(db:Session, details):
    data = {
        "password":details.password,
        "email_address": details.email_address,
        }
    if details.employee_id is None:
        email_exist = db.query(employeeLoginDetails).filter(employeeLoginDetails.email_address == details.email_address).all()
        if email_exist is not None:
            return JSONResponse(status_code=200, content={"status":'success', "detail": "Email already Exist"})    
        db_item = employeeLoginDetails(**data)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return JSONResponse(status_code=200, content={"status":'success', "detail": "Data Save Successfully"})    
    else:
        db_item = db.query(employeeLoginDetails).filter(employeeLoginDetails.employee_id == details.employee_id).first()
        if db_item is None:
            return JSONResponse(status_code=400, content={"status":'success',"detail": "Data is Not exist"})
        db_item.employee_id = details.employee_id
        db_item.email_address = details.email_address
        db_item.password = details.password
        db.commit()
        db.refresh(db_item)
        return JSONResponse(status_code=200, content={"status":'success',"detail": "Data Update Successfully"})
    
def deleteEmpDetails(db:Session, id):
    db_item = db.query(employeeLoginDetails).filter(employeeLoginDetails.employee_id == id.employee_id).first()
    if db_item is None:
        return JSONResponse(status_code=400, content={"status":'success',"detail": "Data of given id is not exist"})
    db.delete(db_item)
    db.commit()
    return JSONResponse(status_code=200, content={"status":'success',"detail": "Data Deleted Successfully", "value":jsonable_encoder(db_item)})

def getEmpdata(db:Session, items):
    db_item = db.query(employeeLoginDetails).order_by(employeeLoginDetails.employee_id.desc())
    db_item = db_item.all()
    if db_item is None:
        return JSONResponse(status_code = 400, content={"status":"success", "details":"Data not Found"})
    return {"status":"success", "details":"Data Found", "result":jsonable_encoder(db_item)}


def getDatabyjoin(db:Session, items:list):
    db_item = db.query(LoginDetails).join(UserDetails, UserDetails.employee_id == LoginDetails.employee_id, isouter=True)
    db_item = db_item.filter(items.employee_id == LoginDetails.employee_id)
    db_item = db_item.all()
    # compiled_query = db_item.statement.compile(compile_kwargs={"literal_binds": True})
    # print(compiled_query)
    return db_item

def batchresult(db:Session, items: List[dict]):
    try:
        db_item  = db.bulk_insert_mappings(employeeLoginDetails, items)  # 1st Traika
        db.commit()
        return JSONResponse(status_code=200, content={"status":'success', "detail": "Data Save Successfully"})    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"LINE: {e.__traceback__.tb_lineno} ERROR: {str(e)}")