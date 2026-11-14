from functions import *
from fastapi import HTTPException


def leave_ride(ride_id: int, roll_no: str):
    session = Session(engine)
    seat = session.query(Seats).filter(
        Seats.ride_id == ride_id,
        Seats.roll_no == roll_no,
        Seats.cancelled == 0
    ).first()

    if seat is None:
        session.close()
        raise HTTPException(status_code=404, detail="Active booking not found for this ride")

    ride = session.query(Rides).filter(Rides.id == ride_id).first()
    if not ride or ride.status in ["cancelled", "completed"]:
        session.close()
        raise HTTPException(status_code=400, detail="Cannot leave ride which is completed or cancelled")

    seat.cancelled = 1
    if ride.seats_left < ride.total_seats:
        ride.seats_left = ride.seats_left + 1

    session.commit()
    session.close()
    return {"message": "Successfully left the ride"}
