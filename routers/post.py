from cProfile import label
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from requests import post
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import models , schemas, oauth2
from  database import get_db




router = APIRouter(
    prefix="/posts",
    tags= ['Posts']
)
#@router.get("/", response_model= List[schemas.Post])
@router.get("/", response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user),
 limit: int = 10 , skip : int = 0, search: Optional[str] = "" ):
    #cursor.execute(""" SELECT * FROM books """)
    #books = cursor.fetchall()
    #print(limit)
    #posts = db.query(models.Books).filter(models.Books.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Books, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Books.id, isouter = True).group_by(models.Books.id).filter(
            models.Books.title.contains(search)).limit(limit).offset(skip).all()
    
    
    return  posts

    

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(book : schemas.PostCreate, db: Session = Depends(get_db),
         current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO books (title, author, synopsis, published ) VALUES (%s, %s, %s, %s) RETURNING
    # * """,
    #            (book.title, book.author, book.synopsis, book.published))

    #new_book = cursor.fetchone()

    #conn.commit()
    
    new_book= models.Books(owner_id=current_user.id, **book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

@router.get("/{id}", response_model= schemas.PostOut)
def get_posts(post_id: int, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM books WHERE id = %s """, (str(id),))
    #book = cursor.fetchone()
    #book = db.query(models.Books).filter(models.Books.id == post_id).first()


    book = db.query(models.Books, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Books.id, isouter = True).group_by(models.Books.id).filter(
            models.Books.id == post_id).first()


    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail = f"post was not found" )
    return book


@router.delete("/{id}")
def delete_post(post_id: int,  db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    
    #cursor.execute("""DELETE FROM books WHERE id = %s returning * """, (str(id)))
    #deleted_book = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Books).filter(models.Books.id == post_id)

    post_id = post_query.first() 
    if post_id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail= f"post with id: {id} does not exist")

    if post_id.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail= f"Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return {'message': "post_id was succefully deleted"}



@router.put("/{id}", response_model= schemas.Post)
def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE books SET title = %s, author = %s, synopsis = %s, published = %s WHERE id = %s RETURNING * """, 
    #(book.title, book.author, book.synopsis, book.published, (str(id))))
    
    #updated_post = cursor.fetchone()
    
    
    #conn.commit()
    
    post_query = db.query(models.Books).filter(models.Books.id == post_id) 


    post = post_query.first()
    
    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail= f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail= f"Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    
    return post_query.first()