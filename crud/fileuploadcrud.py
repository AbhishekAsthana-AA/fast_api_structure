from fastapi import Depends, HTTPException,status
from sqlalchemy.orm import Session
from models.fileupload_modal import fileUploadModal


def saveuploadFile(db:Session,file:list,file_path:str):
    # print(file.type)
    db_user = fileUploadModal(file_name=file.filename, file_path = file_path, 
                              file_type = 'pdf', file_size= file.size,download_count=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def downloadUploadedFile(db:Session, file_id:list):
    if file_id is None:
        raise HTTPException(status_code=404, detail="File id is required")
    db_file = db.query(fileUploadModal).filter(fileUploadModal.id == file_id.file_id)
    return db_file.all()