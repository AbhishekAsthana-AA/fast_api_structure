from database.db import Base
from sqlalchemy import Column, Integer, String


class  Leaves(Base):
    __tablename__ = "leaves"

    id = Column(Integer,primary_key=True,nullable=False)
    leave_id = Column(Integer, index=True)
    leave_name = Column(String, index=True)
    leave_code = Column(String, index=True)