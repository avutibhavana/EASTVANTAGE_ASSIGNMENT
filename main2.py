from numbers import Real
from time import timezone
import schemas,models
from database import SessionLocal,engine
from sqlalchemy.orm import Session
from fastapi import Depends,FastAPI,status,Response
from pydantic import BaseModel

import requests
import urllib.parse

app = FastAPI()

def myCoordinates(address):   
    output = requests.get('https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(str(address)) + '?format=json').json()
    a=[output[0]["lat"] , output[0]["lon"]]
    return a


models.Base.metadata.create_all(engine)

def getDb():
    db= SessionLocal()
    try:
        yield db
    finally:
##db.close() will close the database
        db.close()

#get all the information

@app.get("/getcities")
def get_all(res: Response, db :Session = Depends(getDb)):
    try:
##get all the address data from the database 
        details = db.query(models.Address).all()
        return{"data": details,
                "msg":"fetched successfully!!!!"}
    except Exception as e:
        res.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        return{
            "status":"error occured",
            "msg":str(e)
        }

##post routes i.e., posting the info
@app.post("/postcities")
def createCoordinates(reqbody: schemas.City,res:Response, db :Session = Depends(getDb)):  
    try:
        city = reqbody.city
        state = reqbody.state
        country=reqbody.country
        zipcode = reqbody.zipcode
        address=city,state,country,zipcode
##passing the content into the my coordinates function    
        Data = myCoordinates(address)

        row = models.Address()
##creating the row for the table
        row.city = city
        row.state = state
        row.zipcode = zipcode
        row.country=country
        row.longitude =  Data[0]
        row.latitude =  Data[1]


##adding a row to the table
        db.add(row)
        db.commit()
        return {"data":row,
        "msg":"successfully added!!"}
    except Exception as e:
        res.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status" : "adding failed",
            "msg" : str(e)
        }

##put routes i.e,updating the content
@app.put("/putcities/{cityid}")
def updating(res:Response,reqbody: schemas.City,cityid,db:Session=Depends(getDb)):
    try:   
        city = reqbody.city
        state = reqbody.state
        country=reqbody.country
        zipcode = reqbody.zipcode
        address=city,state,country,zipcode
    
        Data = myCoordinates(address)
##updating the rows with the required fields
        updatedRow ={}
        updatedRow["city"] = city
        updatedRow["state"] = state
        updatedRow["zipcode"]= zipcode
        updatedRow["longitude"] =  Data[0]
        updatedRow["latitude"] = Data[1] 
        
        updating=db.query(models.Address).where(models.Address.id==cityid).update(updatedRow)
        if updating:
    ##   
            db.commit() 
    ##if data updated successfully
            return updating,updatedRow

    ##if data doesnot exist
        else:     
            return "not exists "
    ##error occured enters the except block
    except Exception as e:
        res.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status" : "failed",
            "msg" : str(e)
        }
    
##deleting the information from the content
@app.delete("/deleteingDetails/{cityid}")
def delete(res:Response,cityid,db:Session=Depends(getDb)):
    try:
    ##deleting based on city id
        deleting=db.query(models.Address).where(models.Address.id==cityid).delete()
        

        if deleting:  
            db.commit()  
            print(deleting)
##if the info id successfully deleting
            return {"data":deleting,
                    "msg":"deleting successfully!!!"}
##if the info is not existed      
        else: 
            return "not existed city"

    ##error occured enters the except block
    except Exception as e:
        res.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status" : "failed",
            "msg" : str(e)
        }

# {
#   "city": "bihar",
#   "state": "patna",
#   "country": "string",
#   "zipcode": "400001"
# }









