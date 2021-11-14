from logging import error
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import time
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    

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

my_posts = [{"title": "most hidden cav", "content": "content post 1", "id": 1}, {"title": "most camel country", "content": "content post 2", "id": 2}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

def find_index_post(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "my first api"}

@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM public.posts")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("INSERT INTO public.posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ", (post.title, post.content, post.published))
    new_posts = cursor.fetchone()
    conn.commit()
    return {"data": new_posts}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM public.posts WHERE id = %s", (id,))
    post =  cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM public.posts WHERE id = %s RETURNING *", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    cursor.execute("UPDATE public.posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    return {"post_detail": updated_post}