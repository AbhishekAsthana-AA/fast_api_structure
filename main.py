from fastapi import FastAPI, HTTPException, Depends,Request
from pydantic import BaseModel 
from typing import List, Annotated  
from database.db import Base, engine,check_db_connection
from functools import lru_cache
# from . import config
from router.login import router as login
from router.leaves import router as leave_router
from router.employeeleaves import router as employee_leaves
from router.fileupload import router as file_upload
from crud.logincrud import get_current_user
import time
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(login)
app.include_router(leave_router, dependencies=[Depends(get_current_user)])
app.include_router(employee_leaves, dependencies=[Depends(get_current_user)])
app.include_router(file_upload, dependencies=[Depends(get_current_user)])
Base.metadata.create_all(bind=engine)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
   
    response.headers["X-Process-Time"] = str(process_time)
    return response

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# check for db connection
# @app.on_event("startup")
# async def startup():
#     check_db_connection()

# @app.on_event("shutdown")
# async def shutdown():
#     pass

# @app.get("/bello/{name}")
# async def say_hello(name: str):
#     return {"message": f"bello {name}"}