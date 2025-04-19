#import FastAPI python class that provides all the functionality for your api
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .models import models
from .database import database

database.Base.metadata.create_all(bind=database.engine)

# Create a dependency to get a session or connection to our database


#instantiate a new FastAPI instance
app=FastAPI()

class models(BaseModel):
    title:str
    content:str
    #optional field the user can provide a published if not it will default to True
    published:bool=True


my_posts=[{"title":"api post","content":"content of post 1","id":1},{"title":"api post","content":"content of post 1","id":2}]
#this while is used to connect to the database
#this is for connecting to the database

while True:
    
    try:
        conn=psycopg2.connect(host='localhost',database='newfastapi',user='postgres',password='Bongumenzi#27#',cursor_factory=RealDictCursor)
        #cursor will be used to execute SQL statements
        cursor=conn.cursor()
        print('Database connection was successful')
        #print(cursor)
        break
    
    except Exception as error:
        print("Database connection not successful")
        print('Error:',error)
        #try to connect every two seconds
        time.sleep(2)



def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p


def find_index_posts(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i



@app.get("/login")
async def get_user():
    return {"message":"Hello login to my api"}

@app.get("/posts")
async def get_posts():
    #use cursor to communicate with the database
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()
    print("posts printed")
    print(posts)
    return {"data":posts}
#status code 201 means the post is created successfully

@app.post("/posts",status_code=status.HTTP_201_CREATED)
#validate the incoming data against the Post model, and store the result on new_post variable
async def create_posts(new_post:models):
    #print(new_post)
    #print(new_post.published)
    #take the model and convert it to a standard python dictionary
    #print(new_post.model_dump())
    #post_dict=new_post.model_dump()
    #post_dict['id']=randrange(0,100000)
    #my_posts.append(post_dict)
    
    cursor.execute("""insert into posts (title,content,published) values (%s,%s,%s) returning *""",(new_post.title,new_post.content,new_post.published))
    
    post=cursor.fetchone()
    #push and commit these changes to save in the database
    
    conn.commit()
    
    return {"data":post}

@app.get("/posts/{id}")
#response is of type Response
async def get_post(id:int,response:Response):
    #path parameter
    cursor.execute("""select * from posts where id=%s""",(str(id),))
    post=cursor.fetchone()
    print(post)
    #status code manipulation
    if not post:
        #throw an exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    
        """ response.status_code=status.HTTP_404_NOT_FOUND
        return {"message":f"post with id:{id} not found"} """
    return {"post":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
#status code 204 means nothing should be back to the client
async def delete_post(id:int):
    #find the post to be deleted
    #post=find_post(id)
    cursor.execute("""delete from posts where id=%s returning *""",(str(id),))
    post=cursor.fetchone()
    #commit every change made to the database
    conn.commit()
    #if the post does not exist raise an exception
    if not post:
        #raise an exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} cannot be found")
    #delete the post if it exist
    #find the index
    #index=find_index_posts(id)
    #if index== None:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not content found")
    
    #my_posts.pop(index)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}",status_code=status.HTTP_200_OK)

async def update_posts(id:int,post:models):
    
    cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    
    updated_post=cursor.fetchone()
    
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} could not be found")
    
    return {"post":updated_post}    

@app.put("/new_posts/{id}",status_code=status.HTTP_200_OK)

async def updated_posts(id:int,post:models):
    #find and update the correct post using cursor
    cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    
    #fetch the updated post 
    new_updated_post=cursor.fetchone()
    #commit the new changes to the database
    conn.commit()
    #check if the post does not exists
    if not new_updated_post:
        #raise the excepption
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id={id} is updated")
    #return the updated post
    return {"data":new_updated_post}


