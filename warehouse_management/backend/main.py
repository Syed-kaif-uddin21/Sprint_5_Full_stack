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