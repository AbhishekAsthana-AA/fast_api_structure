from fastapi import Depends, HTTPException,status
from sqlalchemy.orm import Session
from models.leaves_models import Leaves


def get_leave(db: Session):
  # return leave_id
  query = db.query(Leaves)


  result = query.all()
  return result