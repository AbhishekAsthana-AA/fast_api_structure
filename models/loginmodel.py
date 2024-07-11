from database.db import Base
from sqlalchemy import Column, Integer, String

class LoginDetails(Base):
    __tablename__ = 'employee_login'

    employee_id = Column(Integer, primary_key=True, index=True)
    email_address = Column(String, index=True)
    password = Column(String, index=True)

class UserDetails(Base):
     __tablename__ = 'user_details'

     employee_id = Column(Integer, primary_key=True, index=True)
     email_address = Column(String, index= True)
     first_name = Column(String, index=True)
     last_name = Column(String, index=True)
     user_type = Column(String, index=True)
