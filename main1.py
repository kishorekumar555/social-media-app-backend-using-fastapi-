from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from random import randrange
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models,schemas,utils
from database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session
from schemas import Post,Createpost
from fastapi.middleware.cors import CORSMiddleware
# from .routers import users
import sys
sys.path.append( r"D:\server project-1\routers" )
from routers import posts,users,auth,votes
sys.path.append( r"D:\server project-1\config.py")
from config import settings         
print(settings.database_name)
while True:
    try:
        conn=psycopg2.connect(host='localhost',database='Social Media Database(Fast Api project)',user='postgres',password='kishore0510',cursor_factory=RealDictCursor) 
        cursor=conn.cursor()
        print("Database connection was successfull!!!!")
        # cursor.execute("""SELECT * FROM "Posts" """)
        # posts=cursor.fetchall()
        # print(posts)
        break
    except Exception as error:
        print("Connection to database failed!")   
        print("Error:",error) 
        time.sleep(2)
my_posts=[{'id':1,'title':'title for post1','content':'content for post1'},{'id':2,'name':'kumar','age':20}]  
origins=["https://www.google.co.in","https://www.youtube.com"]  
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# @app.get("/posts")
# def getposts():
#     cursor.execute("""SELECT * FROM "Posts" """)
#     posts=cursor.fetchall()
#     # print(posts)
#     return{'message':posts}
# #using ORM get
# @app.get("/sqlalchemy",response_model=List[schemas.PostResponse])
# def get_posts(db:Session=Depends(get_db)):
#     posts=db.query(models.Posts).all()
#     # print(posts)
#     return posts
# # @app.get("/sqlalchemy")
# # def get_posts(db:Session=Depends(get_db)):

# # @app.post("/posts")
# # def posts(gettingposts:Post):
# #     print(gettingposts)
# #     print(gettingposts.dict())
# #     print(gettingposts.title)
# #     print(gettingposts.content)
# #     print(gettingposts.published)
# #     print(gettingposts.rating)
# #     return {'message':'post created successfully'}
# #using ORM post
# @app.post("/sqlalchemy",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
# def create_posts(post:Createpost,db:Session=Depends(get_db)):
#     # new_post=models.Posts(title=post.title,content=post.content,published=post.published,rating=post.rating)
#     new_post=models.Posts(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post
# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# def return_posts(posts:Createpost):
#     # post_dict=posts.dict()
#     # post_dict['id']=randrange(1,20000000)
#     # my_posts.append(post_dict)
#     # print(my_posts)
#     cursor.execute("""INSERT INTO "Posts" ("title","content","published","rating") VALUES(%s, %s, %s, %s) RETURNING * """,(posts.title,posts.content,posts.published,posts.rating))
#     new_post=cursor.fetchone()
#     conn.commit()
#     return{'post':new_post}
# def find_post(id):
#     for p in my_posts:
#        if p['id']==id:
#            return p
# @app.get("/posts/latest")
# def latest_posts():
#     post=my_posts[len(my_posts)-1]
#     return{"latest post":post}
# @app.get("/posts/{id}")#id-string so convert it to integer
# def one_post(id:int):
#     cursor.execute("""SELECT * FROM "Posts" WHERE "id"=%s""",str(id))
#     one_post=cursor.fetchone()
#     if not one_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
#         # response.status_code=status.HTTP_404_NOT_FOUND
#         # return {"Your post":f"post with id:{id} not found"}
#     print(one_post)
#     return{'Your post':one_post}
# #getting one post using orm
# @app.get("/sqlalchemy/{id}",response_model=schemas.PostResponse)
# def get_one_post(id:int,db:Session=Depends(get_db)):
#     post=db.query(models.Posts).filter(models.Posts.id==id).first()
#     return post    
# def find_post_index(id):
#     for i,p in enumerate(my_posts):
#         if p['id']==id:
#             return i
# @app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     cursor.execute("""DELETE FROM "Posts" where "id"=%s returning *""",str(id))
#     deleted_post=cursor.fetchone()
#     conn.commit()
#     if deleted_post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id:{id} not found")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
# # deleting one post using ORM
# @app.delete("/sqlalchemy/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_posts(id:int,db:Session=Depends(get_db)):
#     post=db.query(models.Posts).filter(models.Posts.id==id)
#     if post.first()==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id:{id} not found")
#     post.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
# @app.put("/posts/{id}")
# def update_post(id:int,post:Createpost):
#     cursor.execute("""UPDATE "Posts" SET "title"=%s,"content"=%s,"published"=%s,"rating"=%s where "id"=%s returning *""",(post.title,post.content,post.published,post.rating,str(id)))
#     updated_post=cursor.fetchone()
#     conn.commit()
#     if updated_post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id:{id} not found")
#     return updated_post
# #updating posts using orm
# @app.put("/sqlalchemy/{id}",response_model=schemas.PostResponse)
# def update_post(id:int,post:Createpost,db:Session=Depends(get_db)):
#     post_query=db.query(models.Posts).filter(models.Posts.id==id)
#     up_post=post_query.first()
#     if up_post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id:{id} not found")
#     post_query.update(post.dict(),synchronize_session=False)
#     db.commit()
#     post_query=db.query(models.Posts).filter(models.Posts.id==id).first()
#     return post_query
# @app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.Userout)
# def create_users(user:schemas.Createuser,db:Session=Depends(get_db)):
#     hashed_password=utils.hash(user.password)
#     user.password=hashed_password   
#     new_user=models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user
# #retrieving user details using id
# @app.get("/users/{id}",response_model=schemas.Userout)
# def get_user(id:int,db:Session=Depends(get_db)):
#     user=db.query(models.User).filter(models.User.id==id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id:{id} not found")
#     return user
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)
@app.get("/")
def display():
    return {'message':'Hello world'}



