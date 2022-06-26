from pydantic import BaseModel

##creating a model
class City(BaseModel):
    city: str
    state: str
    country: str
    zipcode: str


