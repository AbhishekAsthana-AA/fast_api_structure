from database.db import Base
from sqlalchemy import Column, Integer, String


class  fileUploadModal(Base):
    __tablename__ = "file_upload_temp"

    id = Column(Integer,primary_key=True,nullable=False)
    file_name = Column(String, index=True)
    file_path = Column(String, index=True)
    file_type = Column(String, index=True)
    file_size = Column(Integer,nullable=False)
    download_count = Column(Integer,nullable=False)