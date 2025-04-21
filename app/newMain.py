from fastapi import FastAPI
#from typing import Optional,List

#from .models import name
from .database import engine,Base
from .routers import post,user,authentication,vote

from fastapi.middleware.cors import CORSMiddleware

#This should create tables inside postgreSQL
#database.Base.metadata.create_all(bind=database.engine)
Base.metadata.create_all(bind=engine)

#instantiate a new FastAPI instance

app=FastAPI(
    title="My Simple API",
    description="Simple API For Production",
    version="2.0.0"
)

#list of domains that can talk to our api
#the origins array shows a list of domains that can talk to our api
#domains that can make requests

origins=["https://google.com",]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=[],
    #allow all http methods to access the api
    allow_methods=["*"],
    #allow all the headers to access the api
    allow_headers=["*"]
)
#include the router object of the post
app.include_router(post.router)
#include the router object of the user 
app.include_router(user.router)
#include the router object for authentication
app.include_router(authentication.router)
#include the router object for vote
app.include_router(vote.router)


@app.get("/rootPath")
def root():
    return {"message":"Hello World"}