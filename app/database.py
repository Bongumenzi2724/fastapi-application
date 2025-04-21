from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
#from .config import settings

#PostgreSQL connection string
SQLALCHEMY_DATABASE_URL=f"postgresql://postgres:Bongumenzi#27#@localhost/newfastapi"

#responsible for create a postgresql connection
engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()
# Create a dependency to get a session or connection to our database

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


