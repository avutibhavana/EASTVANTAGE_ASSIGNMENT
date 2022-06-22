# from numbers import Real
# from time import timezone
# from fastapi import FastAPI
# from pydantic import BaseModel

# import requests

# import urllib.parse

# app = FastAPI()

# db = []

# # address = 'Shivaji Nagar, Bangalore, KA 560001'
# # url = 'https://nominatim.openstreetmap.org/search/' + \
# #     urllib.parse.quote(address) + '?format=json'
# # response_location = requests.get(url).json()
# # print(response_location[0]["lat"])
# # print(response_location[0]["lon"])
# # {
# #     "city": "Nagpur",
# #     "state": "Maharashtra",
# #     "country": "India",
# #     "zipcode": "440001"
# # }


# class City(BaseModel):
#     city: str
#     state: str
#     country: str
#     zipcode: str


# @app.get('/')
# def index():
#     return {'key': 'value'}


# @app.get('/cities')
# async def get_cities():
#     results = []
#     for address in db:
#         address_var = (address['city'], ' , ', address['state'],
#                        ' , ',   address['country'], ' , ', address['zipcode'])
#         print(address_var)
#         r = requests.get(
#             f'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(str(address_var)) + '?format=json')
#         response_location = r.json()
       
#         results.append(
#             {'city': address['city'], 'state': address['state'], 'country': address['country'], 'zipcode': address['zipcode'], 'latitude': response_location[0]["lat"], 'longitude': response_location[0]["lon"]})
#     print(results,"bhavana")

#     return results


# @app.get('/cities/{city_id}')
# def get_city(city_id: int):
#     print(city_id)
#     address = db[city_id-1]
#     address_var = (address['city'], ' , ', address['state'],
#                    ' , ',   address['country'], ' , ', address['zipcode'])
#     #print('address:, ', address, address_var)
#     r = requests.get(
#         f'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(str(address_var)) + '?format=json')
#     response_location = r.json()
#     return {'city': address['city'], 'state': address['state'], 'country': address['country'], 'zipcode': address['zipcode'], 'latitude': response_location[0]["lat"], 'longitude': response_location[0]["lon"]}


# @app.post('/cities')
# async def create_city(city: City):
#     db.append(city.dict())
#     return db[-1]


# @app.put("/cities/{city_id}")
# async def update_city(city_id: int, city: City):
#     put_address = city.dict()
#     print(put_address, city.dict())
#     return {"city_id": city_id, **put_address}


# @app.delete('/cities/{city_id}')
# def delete_city(city_id: int):
#     db.pop(city_id-1)
#     return {}

# # {
# #   "city": "bihar",
# #   "state": "patna",
# #   "country": "string",
# #   "zipcode": "400001"
# # }


from numbers import Real
from time import timezone
from fastapi import FastAPI,Depends
import schemas,models
from database import engine,SessionLocal
from sqlalchemy.orm import Session


import requests

import urllib.parse

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()

db = []

# address = 'Shivaji Nagar, Bangalore, KA 560001'
# url = 'https://nominatim.openstreetmap.org/search/' + \
#     urllib.parse.quote(address) + '?format=json'
# response_location = requests.get(url).json()
# print(response_location[0]["lat"])
# print(response_location[0]["lon"])
# {
#     "city": "Nagpur",
#     "state": "Maharashtra",
#     "country": "India",
#     "zipcode": "440001"
# }




@app.get('/')
def index():
    return {'key': 'value'}


@app.get('/cities')
async def get_cities():
    results = []
    for address in db:
        address_var = (address['city'], ' , ', address['state'],
                       ' , ',   address['country'], ' , ', address['zipcode'])
        print(address_var)
        r = requests.get(
            f'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(str(address_var)) + '?format=json')
        response_location = r.json()
       
        results.append(
            {'city': address['city'], 'state': address['state'], 'country': address['country'], 'zipcode': address['zipcode'], 'latitude': response_location[0]["lat"], 'longitude': response_location[0]["lon"]})
    print(results,"bhavana")

    return results


@app.get('/cities/{city_id}')
def get_city(city_id: int):
    print(city_id)
    address = db[city_id-1]
    address_var = (address['city'], ' , ', address['state'],
                   ' , ',   address['country'], ' , ', address['zipcode'])
    #print('address:, ', address, address_var)
    r = requests.get(
        f'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(str(address_var)) + '?format=json')
    response_location = r.json()
    return {'city': address['city'], 'state': address['state'], 'country': address['country'], 'zipcode': address['zipcode'], 'latitude': response_location[0]["lat"], 'longitude': response_location[0]["lon"]}


@app.post('/cities')
def create_city(request: schemas.City,db:Session=Depends(get_db)):
  
    new_city=models.Address(
        addressLine=request.addressLine,
        city=request.city,
        state=request.state,
        zipcode=request.zipcode
        )
    db.add(new_city)
    db.add(new_city)
    db.refresh(new_city)

    return {
            "status": "ok",
            "data": new_city
        }
        
    # db.append(city.dict())
    # return db[-1]


@app.put("/cities/{city_id}")
async def update_city(city_id: int, city: schemas.City):
    put_address = city.dict()
    print(put_address, city.dict())
    return {"city_id": city_id, **put_address}


@app.delete('/cities/{city_id}')
def delete_city(city_id: int):
    db.pop(city_id-1)
    return {}

# {
#   "city": "bihar",
#   "state": "patna",
#   "country": "string",
#   "zipcode": "400001"
# }