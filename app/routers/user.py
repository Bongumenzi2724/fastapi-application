from fastapi import Response,status,HTTPException,Depends,APIRouter
from ..schemas import UserSchema,UserResponse
from typing import List
from ..database import get_db
from ..models import User
from ..utils import hashpassword,verify_user
from sqlalchemy.orm import Session

#create a router object
router=APIRouter(
    prefix="/new_users",
    tags=['Users']
)


#create a new user
@router.post("",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
async def create_user(user:UserSchema,db:Session=Depends(get_db)):
    #save the new password in the user object
    user.password=hashpassword(user.password)
    #open a database session and create a new user
    new_user=User(**user.model_dump())
    #add the new user to the database
    db.add(new_user)
    #commit the new user to the database
    db.commit()
    #return the committed user using refresh
    db.refresh(new_user)
    #return the user created
    return new_user

#fetch all users
@router.get("",status_code=status.HTTP_200_OK,response_model=List[UserResponse])
async def get_users(db:Session=Depends(get_db)):
    #query the database for 
    all_users=db.query(User).all()
    return all_users

@router.post("/login",status_code=status.HTTP_200_OK)
async def user_login(user:UserSchema,db:Session=Depends(get_db)):
    #retrieve the password from the user object
    user=verify_user(user.password)
    print(f"true if the password is verified:{user}")
    #if the user is not verified raise an exception
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"user not authorized to login")
    #find the user and return the user email
    new_user=db.query(User).filter(user.id).first()
    
    return new_user.email

#Get the user from the database, we need a response model

@router.get("/{id}",status_code=status.HTTP_200_OK)
async def get_user(id:int,db:Session=Depends(get_db)):
    #query the user
    new_user=db.query(User).filter(User.id==id).first()
    #raise an exception if the user is not found
    if not new_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id:{id} does not exist")
    
    return new_user