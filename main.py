import py_compile
from typing import Optional, List
from fastapi import FastAPI
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
import models , schemas, utils
from  database import engine, get_db
from routers import post, user, auth


models.Base.metadata.create_all(bind = engine) 

app = FastAPI()


while True:    
    try:
        conn = psycopg2.connect(host= 'localhost', database= 'db', user= 'postgres',
        password= 'Jaredcaleb#1', cursor_factory=RealDictCursor)   
        cursor = conn.cursor()
        print("Database connection was succesfull!!!")
        break
    except Exception as error:
        print('Connecting to Database failed')
        print("Error: ", error)
        time.sleep(2)
    

my_posts = [{"title": "title of Book 1", "author": "author of book 1", "id": 7}, {
    "title": "title of Book 2", "author": "author of book 2",  "id": 3}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def server():
    return {'server running well!!!!'}


