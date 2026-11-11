from fastapi import FastAPI, HTTPException
from sqlalchemy.testing.pickleable import User

import function

app = FastAPI()

@app.post("/register")
def register(name:str, destination:str, weight:float, status:str):
    return function.register_package(name=name, destination=destination, weight=weight,  status=status)


@app.get("/packages")
def get_registration():
    return function.get_registration()

@app.get("/packages/filter")
def filter_package(destination=None, status=None, arrival_date=None):
    return function.filter_package(destination=destination, status=status, arrival_date=arrival_date)

@app.get("/packages/{package_id}")
def get_specific_package(package_id:int):
    return function.get_specific_package(package_id=package_id)

@app.patch("/packages/update")
def update_package(package_id:int, weight:float, destination :str, status:str):
    return function.update_package(package_id=package_id, weight=weight, destination=destination, status=status)

@app.delete("/packages/{package_id}")
def delete_package(package_id:int):
    return function.delete_specific_package(package_id=package_id)