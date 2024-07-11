from pydantic import BaseModel,validator
from datetime import date
from typing import Optional

class employeeLeaves(BaseModel):
    start_date:Optional[date] = None
    end_date:Optional[date] = None
    @validator('start_date', 'end_date', pre=True, always=True)
    def convert_blank_to_none(cls, v):
        if v == '':
            return None
        return v
    
class employeeLoginPayload(BaseModel):
    employee_id:Optional[int] = None
    email_address:str
    password:str

class deleteLoginPayload(BaseModel):
    employee_id:int


class batchInsert(BaseModel):
    data:list