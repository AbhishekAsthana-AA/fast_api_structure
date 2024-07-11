from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import List

from database.db import get_db
from fastapi import APIRouter
from models.leaves_models import Leaves
from schema.leaves_details import LeavesSchema, InserLeaveSchema,DeleteLeaveSchema
from crud.leavescrud import get_leave

router = APIRouter()

@router.post("/readLeaves")
def read_leave(db: Session = Depends(get_db)):
    db_leave = get_leave(db)
    if db_leave is None:
        raise HTTPException(status_code=200, detail="Leave not found")
    return [db_leave]
