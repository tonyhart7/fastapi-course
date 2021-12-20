from logging import error
import time

from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

import models
from database import engine
from router import post , user , auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(dbname='fastapi', user='postgres', password='superucer123', host='localhost', cursor_factory=RealDictCursor) 
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error :
        print("Connection was failed")
        print("Error: ", error)
        time.sleep(3)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "my first api"}
