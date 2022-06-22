from database import Base
from sqlalchemy import Column,Integer,String,Float


## creating a table for database
##creating all the columns in database


class Address(Base):
    __tablename__="address"

   
    id = Column(Integer, primary_key=True, index=True)
    addressLine = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    zipcode = Column(Integer)
    longitude = Column(Float)
    latitude = Column(Float)
   





