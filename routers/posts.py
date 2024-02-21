# from ..import schemas,models,utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
# from..database import get_db
from typing import List,Optional
import sys
sys.path.append( r"D:\Server Project-2" )
import schemas,models,utils,database,oauth2
from database import get_db
router=APIRouter()

@router.get("/sqlalchemy",response_model=List[schemas.PostVote])
def get_posts(db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    # print(limit)
    # posts=db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    posts=db.query(models.Posts,func.count(models.Vote.posts_id).label("likes")).join(models.Vote,models.Vote.posts_id==models.Posts.id,isouter=True).group_by(models.Posts.id).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    # print(posts)
    return posts

@router.post("/sqlalchemy",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post:schemas.Createpost,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # new_post=models.Posts(title=post.title,content=post.content,published=post.published,rating=post.rating)
    # print(current_user)
    # user_query=db.query(models.User).filter(models.User.id==current_user).first()
    # print(user_query.email)
    # print(current_user.email)
    new_post=models.Posts(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/sqlalchemy/{id}",response_model=schemas.PostResponse)
def get_one_post(id:int,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    #print(current_user)
    post=db.query(models.Posts).filter(models.Posts.id==id).first()
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    return post    

@router.delete("/sqlalchemy/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    print(current_user)
    post_query=db.query(models.Posts).filter(models.Posts.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id:{id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/sqlalchemy/{id}",response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.Createpost,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    print(current_user)
    # user_query=db.query(models.User).filter(models.User.id==current_user).first()
    post_query=db.query(models.Posts).filter(models.Posts.id==id)
    up_post=post_query.first()
    if up_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id:{id} not found")
    if up_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    post_query=db.query(models.Posts).filter(models.Posts.id==id).first()
    return post_query