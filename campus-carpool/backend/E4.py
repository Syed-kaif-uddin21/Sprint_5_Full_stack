from functions import *
from fastapi import HTTPException
from pydantic import BaseModel


def cancel_ride(ride_id: int, driver_roll: str):
    session = Session(engine)
    ride = session.query(Rides).filter(Rides.id == ride_id, Rides.driver_roll == driver_roll).first()

    if not ride:
        session.close()
        raise HTTPException(status_code=404, detail="Ride not found (check ride_id and driver_roll)")

    if ride.status != "scheduled":
        session.close()
        raise HTTPException(status_code=400, detail="This ride is currently not scheduled")

    seats = session.query(Seats).filter(Seats.ride_id == ride.id).all()
    for seat in seats:
        seat.cancelled = 1

    ride.status = "cancelled"
    session.commit()
    session.close()
    return {"message": "Ride cancelled successfully"}


def get_rides():
    session = Session(engine)
    rides = session.query(Rides).all()
    session.close()
    return rides
