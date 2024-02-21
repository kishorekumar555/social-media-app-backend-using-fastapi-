# from..import schemas,models,utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
# from..database import get_db
import sys
sys.path.append( r"D:\Server Project-2" )
import schemas,models,utils,database
from database import get_db
router=APIRouter()
@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.Userout)
def create_users(user:schemas.Createuser,db:Session=Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password   
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
#retrieving user details using id
@router.get("/users/{id}",response_model=schemas.Userout)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id:{id} not found")
    return user