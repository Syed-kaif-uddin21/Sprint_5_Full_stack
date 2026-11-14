from functions import *
from fastapi import HTTPException
from datetime import date

def complete_ride(driver_roll: str, ride_id: int):
    session = Session(engine)
    ride = session.query(Rides).filter(Rides.id == ride_id).first()
    if not ride:
        session.close()
        raise HTTPException(status_code=404, detail="Ride not found")
    if ride.driver_roll != driver_roll:
        session.close()
        raise HTTPException(status_code=403, detail="You're not allowed to do this")
    if ride.status != "scheduled":
        session.close()
        raise HTTPException(status_code=400, detail="Ride is not scheduled")

    today = date.today()
    ride_d = ride.ride_date
    if isinstance(ride_d, str):
        ride_d = date.fromisoformat(ride_d)

    if ride_d > today:
        session.close()
        raise HTTPException(status_code=400, detail="Cannot complete ride before its date")

    ride.status = "completed"
    session.commit()
    session.close()
    return {"message": "Ride completed successfully"}
