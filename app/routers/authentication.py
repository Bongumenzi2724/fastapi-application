from fastapi import status,HTTPException,Depends,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..schemas import UserSchema,Token
from ..database import get_db
from ..models import User
from ..utils import verify_user
from ..authentication import oauth2

router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

#login route
@router.post("/login",status_code=status.HTTP_200_OK,response_model=Token)
#pass the schema definition for request object validation and the database(db) variable to open session with the database
async def login(user:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    #get the password and email from the request object using a database session
    
    #query the database for the user using the email from the request object
    new_user=db.query(User).filter(User.email==user.username)
    #raise the exception if the user is not found
    if not new_user.first():
        #raise the exception
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credentials")
    
    #hash the password from the user
    
    #compare the password and raise an exception if the hashed passwords are not the same
    if not verify_user(user.password,new_user.first().password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credentials")
    
    #create a token
    access_token=oauth2.create_access_token(data={"user_id":new_user.first().id})
    
    #if allowed access the account and return a token
    
    return {"access_token":access_token,"token_type":"bearer token"}

#register user
@router.post("/register",status_code=status.HTTP_200_OK)
async def register_user(user:UserSchema,db:Session=Depends(get_db)):
    return{"status":"registered"}