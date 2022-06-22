from pydantic import BaseModel




class City(BaseModel):
    city: str
    state: str
    country: str
    zipcode: str