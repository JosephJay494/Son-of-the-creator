from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models , schemas
from  database import get_db




router = APIRouter(
    prefix="/posts",
    tags= ['Posts']
)

@router.get("/", response_model= List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM books """)
    #books = cursor.fetchall()

    posts = db.query(models.Books).all()
    return  posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
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

@router.get("/{id}", response_model= schemas.Post)
def get_posts(post_id: int, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM books WHERE id = %s """, (str(id),))
    #book = cursor.fetchone()
    book = db.query(models.Books).filter(models.Books.id == post_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail = "post was not found" )
    return book


@router.delete("/{id}")
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



@router.put("/{id}", response_model= schemas.Post)
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