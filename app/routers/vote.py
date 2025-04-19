from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import VoteSchema
from ..authentication import oauth2
from ..models import Votes,Post

#create router instance
router=APIRouter(
    prefix="/vote",
    tags=["Votes"]
)

#create the vote route
@router.post("",status_code=status.HTTP_201_CREATED)
async def vote(vote:VoteSchema,db:Session=Depends(get_db),user:int=Depends(oauth2.get_current_user)):
    #query for post
    post=db.query(Post).filter(Post.id==vote.post_id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{vote.post_id} does not exist")
    
    vote_query=db.query(Votes).filter(Votes.post_id == vote.post_id,Votes.user_id==user.id)
    #get the vote that matches
    found_vote=vote_query.first()
    
    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user with id:{user.id} has already voted on post {vote.post_id}")
        new_vote=Votes(post_id=vote.post_id,user_id=user.id)
        #add the vote
        db.add(new_vote)
        #commit the vote
        db.commit()
        return {"message":"successfully added vote"}
    elif vote.dir==0:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Vote does not exist")
        vote_query.delete(synchronize_session=False)
        #commit the changes in the database
        db.commit()
        return {"message":"successfully deleted vote"}
    
    else:
        return {"message":"value not allowed for vote, use 1 or 0"}
    
