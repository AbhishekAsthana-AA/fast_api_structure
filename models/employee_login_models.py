from sqlalchemy import Column, Integer, String,DOUBLE_PRECISION,TIMESTAMP, Date
from database.db import Base

class employeeLoginDetails(Base):
    __tablename__= 'farzi_table'

    employee_id = Column(Integer, primary_key=True, index=True)
    email_address =  Column(String, index=True)
    password = Column(String, index=True)