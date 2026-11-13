from fastapi import FastAPI, HTTPException, Header, Body
from pydantic import BaseModel
import function
from typing import Optional

app = FastAPI()

class Package(BaseModel):
    name: str
    destination: str
    weight: float
    status: str
    arrival_date: str

class UpdatePackage(BaseModel):
    package_id: int
    weight: Optional[float] = None
    destination: Optional[str] = None
    status: Optional[str] = None

@app.post("/register")
def register(package:Package, token = Header(None)):
    username = function.verify_token(token, "access")
    if not username:
        raise HTTPException(status_code=401)
    return function.register_package(name=package.name, destination=package.destination, weight=package.weight,  status=package.status)


@app.get("/packages")
def get_registration(token = Header(None)):
    username = function.verify_token(token, "access")
    if not username :
        raise HTTPException(status_code=401)
    return function.get_registration()

@app.get("/packages/filter")
def filter_package(destination: str = None, status:str = None, arrival_date: str = None, token = Header(None)):
    username = function.verify_token(token, "access")
    if not username :
        raise HTTPException(status_code=401)
    return function.filter_package(destination=destination, status=status, arrival_date=arrival_date)

@app.get("/packages/{package_id}")
def get_specific_package(package_id:int,token = Header(None)):
    username = function.verify_token(token, "access")
    if not username:
        raise HTTPException(status_code=401)
    return function.get_specific_package(package_id=package_id)

@app.patch("/packages/update")
def update_package(update_data: UpdatePackage, token = Header(None)):
    username = function.verify_token(token, "access")
    if not username:
        raise HTTPException(status_code=401)
    return function.update_package(package_id=update_data.package_id, weight=update_data.weight, destination=update_data.destination, status=update_data.status)

@app.delete("/packages/{package_id}")
def delete_package(package_id:int, token = Header(None)):
    username = function.verify_token(token, "access")
    if not username:
        raise HTTPException(status_code=401)
    return function.delete_specific_package(package_id=package_id)

@app.get("/batches/filter")
def filter_batch(destination:str =None, vehicle:str =None, dispatch_status:str =None,token = Header(None)):
    username = function.verify_token(token, "access")
    if not username:
        raise HTTPException(status_code=401)
    return function.filter_batch(destination=destination, vehicle=vehicle, dispatch_status=dispatch_status)

@app.get("/batches/summary")
def summary(token = Header(None)):
    username = function.verify_token(token, "access")
    if not username:
        raise HTTPException(status_code=401)
    return function.dispatch_summary()

@app.post("/login")
def login(username=Body(), password=Body()):
    token = function.verify_login(username=username, password=password)
    if not token:
        raise HTTPException(status_code=401)
    return {"token" : token}

@app.post("/refresh")
def refresh(refresh_token):
    username = function.verify_token(token=refresh_token,token_type="refresh")
    if not username:
        raise HTTPException(status_code=401, detail="token is invalid")

    access_token = function.create_token(username=username,token_type="access")
    return {"access_token" : access_token}

@app.post("/register_user")
def register_user(username = Body(), password = Body()):
    if function.register_user(username=username, password=password):
        return ("message : user registration successful")
    raise HTTPException(status_code=401, detail="User already exists")