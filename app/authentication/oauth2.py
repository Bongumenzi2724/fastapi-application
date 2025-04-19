from jose import JWTError,jwt
from fastapi import Depends,status,HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta,timezone
from ..schemas import TokenData
from ..database import get_db
from ..models import User
#from ..config import settings

#give a secret key
#SECRET_KEY=settings.secret_key

SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
#provide an algorithm for producing the token
#ALGORITHM=settings.algorithm
ALGORITHM="HS256"
#provide an expiration time in minutes
#EXPIRATION_TIME=settings.access_token_expire_minutes
EXPIRATION_TIME=30

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data:dict):
    #make a copy of the data to prevent corruption
    to_encode=data.copy()
    #create the expiration time of the token
    expire=datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_TIME)
    #add the expire property into the initial data
    to_encode.update({"exp":expire})
    #encode the jwt token
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    #return the encoded jwt
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
       
        id:str=payload.get("user_id")
       
        if id is None:
            raise credentials_exception
        #what is this??
        #token_data=TokenData(id=id)
        #print(token_data)
        
    except JWTError as e:
        print("an exception occurred while authenticating the user")
        print(e)
        raise credentials_exception
    #return the token data
    return id

#can be passed as a dependency,takes a token extracts the id from token and verify the token using verify_access_token method
#Used for route protection and fetching the user after authentication

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    #create the credentials exception object
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    #verify the access token and get the user id
    token=verify_access_token(token,credentials_exception)
    #fetch the current user
    current_user=db.query(User).filter(User.id==token).first()
    
    return current_user


