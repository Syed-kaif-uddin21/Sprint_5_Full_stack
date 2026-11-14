from functions import *
from fastapi import HTTPException


def student_rides(roll_no: str):
    session = Session(engine)
    driving = session.query(Rides).filter(Rides.driver_roll == roll_no).all()
    joined = session.query(Rides).join(Seats, Seats.ride_id == Rides.id).filter(Seats.roll_no == roll_no, Seats.cancelled == 0 ).all()
    session.close()
    return {"driving": driving,"joined": joined}