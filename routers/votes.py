from fastapi import FastAPI,APIRouter,HTTPException,status,Depends,Response
import database,oauth2,schemas,models
from sqlalchemy.orm import Session
router=APIRouter(
    prefix="/vote",
    tags=['Vote']
)
@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    post=db.query(models.Posts).filter(models.Posts.id==vote.posts_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id:{vote.posts_id} is not found")
    vote_query=db.query(models.Vote).filter(models.Vote.posts_id==vote.posts_id,models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()
    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted the post {vote.posts_id}")
        new_vote=models.Vote(posts_id=vote.posts_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Successfully deleted vote"}    