from pydantic import BaseModel
from typing import Optional


class LeavesSchema(BaseModel):
    # id: int
    leave_id: int
    # leave_name: str
    # leave_code: str

# class Config:
#     # from_attributes = True
#     orm_mode = True

class InserLeaveSchema(BaseModel):
     id: Optional[int] = None
     leave_id: int
     leave_name: str
     leave_code: str

class DeleteLeaveSchema(BaseModel):
     id: int