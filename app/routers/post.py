from fastapi import Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from typing import List,Optional
from ..schemas import PostResponse,CreatePost,UpdatePost,PostOut
from ..models import Votes,Post
from ..authentication import oauth2
from ..database import get_db

#Create a router object
router=APIRouter(
    prefix="/new_posts",
    tags=['Posts']
)


#use join to fetch data
@router.get("/joins",status_code=status.HTTP_200_OK,response_model=List[PostOut])
async def get_posts_with_joins(db:Session=Depends(get_db),user:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=" "):
    #print the user
    print(user.email)
    print(user.id)
    #querry data with the model post
    results=db.query(Post,func.count(Votes.post_id).label("votes")).join(Votes,Votes.post_id==Post.id,isouter=True).group_by(Post.id).all()
      
    print(results)
    
    return results

#Get all posts,the default limit is 10
@router.get("",status_code=status.HTTP_200_OK,response_model=List[PostResponse])
async def get_posts(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    
    print(skip)
    print(limit)
    #%20 means space in the url
    
    print(f"the search keyword: {search}")
    
    #query the database for the new object
    new_posts=db.query(Post).filter(Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #new_posts is returned as an array of objects
    return new_posts


#create a new post using an orm
@router.post("",status_code=status.HTTP_201_CREATED)
async def create_new_post(post:CreatePost,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    #open a database session to create a new database entity
    #the owner id is in user_id variable
    print(f"user id is:{user_id.id}")
    
    new_post=Post(owner_id=user_id.id,**post.model_dump())
    #create a post by opening a database session and committing a new entity
    #add the new data into the database
    #print(post.model_dump())
    #add the owner id in the new_post
    db.add(new_post)
    #commit the new entry in the current session
    db.commit()
    #return the committed entry
    db.refresh(new_post)
    #return the post to the client
    return {"data":new_post}

#Querying an individual post
@router.get("/{id}",status_code=status.HTTP_200_OK)
async def get_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #open a databse session and fetch the first post with a matching id
    new_post=db.query(Post).filter(Post.id==id).first()
    
    #if the post is not found raise an exception
    if not new_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} is not found")
    
    return new_post
    
#delete the first post with a matching id
@router.delete("/{id}",status_code=status.HTTP_200_OK)
async def delete_post(id:int,db:Session=Depends(get_db),user:int=Depends(oauth2.get_current_user)):
    #query the database for the post with a matching id
    deleted_post=db.query(Post).filter(Post.id==id)
    #raise an exception if the post is not found
    
    if not deleted_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} is not found")
    
    
    if deleted_post.first().owner_id !=user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"this post is not yours bro")
    #delete the post if it exist
    deleted_post.delete(synchronize_session=False)
    #to make database changes you have to commit
    db.commit()
    return{"message":f"post with id:{id} successfully deleted"}

#update the post with a matching id
@router.patch("/{id}",status_code=status.HTTP_201_CREATED,response_model=PostResponse)
async def update_post(id:int,post:UpdatePost,db:Session=Depends(get_db),user:int=Depends(oauth2.get_current_user)):
    #find the post to update
    updated_post=db.query(Post).filter(Post.id==id)
    #raise an exception if the post does not exist
    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    
    #make sure the user is updating a post that belongs to them
    
    if not updated_post.first().owner_id==user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not allowed to update this post") 
    
    #update the post
    updated_post.update(post.model_dump(),synchronize_session=False)
    #commit the changes to the database
    db.commit()
    return {"data":updated_post.first()}
