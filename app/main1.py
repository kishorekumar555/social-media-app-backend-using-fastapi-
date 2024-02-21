from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
class Post(BaseModel):#schema for Post method
    title:str
    content:str
    published:bool=True
    rating:Optional[int]=None
my_posts=[{'id':1,'title':'title for post1','content':'content for post1'},{'id':2,'name':'kumar','age':20}]    
app=FastAPI()
@app.get("/posts")
def getposts():
    return{'message':my_posts}
# @app.post("/posts")
# def posts(gettingposts:Post):
#     print(gettingposts)
#     print(gettingposts.dict())
#     print(gettingposts.title)
#     print(gettingposts.content)
#     print(gettingposts.published)
#     print(gettingposts.rating)
#     return {'message':'post created successfully'}
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def return_posts(posts:Post):
    post_dict=posts.dict()
    post_dict['id']=randrange(1,20000000)
    my_posts.append(post_dict)
    print(my_posts)
    return{'posts':post_dict}
def find_post(id):
    for p in my_posts:
       if p['id']==id:
           return p
@app.get("/posts/latest")
def latest_posts():
    post=my_posts[len(my_posts)-1]
    return{"latest post":post}
@app.get("/posts/{id}")#id-string so convert it to integer
def one_post(id:int,response:Response):
    one_post=find_post(id)
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"Your post":f"post with id:{id} not found"}
    print(one_post)
    return{'Your post':one_post}
def find_post_index(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index=find_post_index(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id:{id} not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    index=find_post_index(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id:{id} not found")
    updated_post=post.dict()
    updated_post['id']=id
    my_posts[index]=updated_post
    return {'Your updated post':updated_post}

