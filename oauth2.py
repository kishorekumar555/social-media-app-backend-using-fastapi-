from jose import JWTError,jwt
from datetime import datetime,timedelta
import schemas,database,models
from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config import settings
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY=settings.secret_key
ALGORITHM =settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
def verify_access_token(token:str,credentials_exception):
    try:
       decode_data=jwt.decode(token,SECRET_KEY,[ALGORITHM])
       id:str=decode_data.get("user_id")
       if id is None:
          raise credentials_exception
       token_data=schemas.TokenData.id=id
    except JWTError:
        raise credentials_exception
    return token_data
#creating dependency function
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not Validate your account",headers={"WWW-Authenticate":"Bearer"})
    Token= verify_access_token(token,credentials_exception)
    print(Token)
    user=db.query(models.User).filter(models.User.id==Token).first()
    return user