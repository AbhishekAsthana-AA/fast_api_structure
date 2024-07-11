from sqlalchemy import Column, Integer, String,DOUBLE_PRECISION,TIMESTAMP, Date
from database.db import Base

class employeeLeaveDetails(Base):
    __tablename__= 'employee_leaves'

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, index=True)
    start_date = Column(Date, index=True)
    end_date = Column(Date, index=True)
    total_days = Column(DOUBLE_PRECISION, index=True)
    leave_id = Column(String, index=True)


