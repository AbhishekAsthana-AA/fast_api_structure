from fastapi import Depends, HTTPException, APIRouter, File,UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import List
import os
from database.db import get_db
from crud.fileuploadcrud import saveuploadFile, downloadUploadedFile
from schema.file_upload import DownloadFileSchema
router = APIRouter()

@router.post("/fileupload")
def uploadFileData(file: UploadFile = File(...), db:Session = Depends(get_db)):

     try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        upload_dir = os.path.join(base_dir, 'src', 'uploads', 'downloads')
        if not os.path.exists(upload_dir):
          os.makedirs(upload_dir)

        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
            file_size = os.path.getsize(file_path)

        result = saveuploadFile(db,file,file_path)
        if result is None:
           raise HTTPException(status_code=200, detail="File not upload")
        return result
     except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
     
@router.post("/downloadfile")
def downloadFile(file_id: DownloadFileSchema, db:Session= Depends(get_db)):
    res = downloadUploadedFile(db, file_id)
    if res is None:
       raise HTTPException(status_code=400, detail="File not found")
    file_path = res[0].file_path
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on server")
    file_name = os.path.basename(file_path)
    return {"file_path":file_path, "file_name":file_name}
