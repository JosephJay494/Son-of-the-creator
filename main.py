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


@app.get("/")
def server():
    return {'server running well!!!!'}

@app.get("/posts", response_model= List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM books """)
    #books = cursor.fetchall()

    posts = db.query(models.Books).all()
    return  posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(book : schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO books (title, author, synopsis, published ) VALUES (%s, %s, %s, %s) RETURNING
    # * """,
    #            (book.title, book.author, book.synopsis, book.published))

    #new_book = cursor.fetchone()

    #conn.commit()

    new_book = models.Books(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

@app.get("/post/{id}", response_model= schemas.Post)
def get_posts(post_id: int, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM books WHERE id = %s """, (str(id),))
    #book = cursor.fetchone()
    book = db.query(models.Books).filter(models.Books.id == post_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail = "post was not found" )
    return book


@app.delete("/post/{id}")
def delete_post(post_id: int,  db: Session = Depends(get_db)):
    
    #cursor.execute("""DELETE FROM books WHERE id = %s returning * """, (str(id)))
    #deleted_book = cursor.fetchone()
    #conn.commit()
    post = db.query(models.Books).filter(models.Books.id == post_id) 
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail= f"post with id: {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()

    return {'message': "post was succefully deleted"}



@app.put("/post/{id}", response_model= schemas.Post)
def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE books SET title = %s, author = %s, synopsis = %s, published = %s WHERE id = %s RETURNING * """, 
    #(book.title, book.author, book.synopsis, book.published, (str(id))))
    
    #updated_post = cursor.fetchone()
    
    
    #conn.commit()
    
    post_query = db.query(models.Books).filter(models.Books.id == post_id) 


    post = post_query.first()
    
    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail= f"post with id: {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    
    return post_query.first()

@app.post("/user", status_code=status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):


    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user= models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users/{id}", response_model=schemas.UserOut)
def get_users(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail = f"User with id: {id} does not exits" )
    return user
