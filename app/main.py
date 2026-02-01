from typing import Optional, List
from fastapi.params import Body
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .db import models
from .schemas import schemas
from .db.database import  engine, get_db
from .base.utils import hash_password
from .routes import post,user, auth
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastAPI-app', user='postgres',
                                password='root', cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        break
    except Exception as error:
        print("Conn to database failed")
        print("error: ", error)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)






