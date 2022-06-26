# SQLAlchemy is an open-source SQL toolkit and object-relational mapper
#  for the Python programming language
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

##using sql alchemy initializing the data base
SQLALCHEMY_DATABASE_URL='sqlite:///./cities.db'

engine=create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

##session maker will generate a new session object everytime when we call the database

SessionLocal = sessionmaker( bind=engine,autocommit=False, autoflush=False)
# declarative_base () is a factory function that constructs a
#  base class for declarative class definitions 
Base = declarative_base()









