from functions import *
from fastapi import HTTPException
from datetime import date


def join_ride(ride_id, roll_no):
    session = Session(engine)

    ride = session.query(Rides).filter(Rides.id == ride_id).first()
    if not ride:
        session.close()
        raise HTTPException(status_code=404, detail="Ride not found")

    if ride.driver_roll == roll_no:
        session.close()
        raise HTTPException(status_code=400, detail="Cannot book own ride")

    ride_d = ride.ride_date
    if isinstance(ride_d, str):
        ride_d = date.fromisoformat(ride_d)

    if ride.status in ["cancelled", "completed"] or ride_d < date.today():
        session.close()
        raise HTTPException(status_code=400, detail="Ride not available")

    if ride.seats_left <= 0:
        session.close()
        raise HTTPException(status_code=400, detail="Ride has no seats left")

    seats = session.query(Seats).filter(Seats.ride_id == ride_id).all()
    for seat in seats:
        if seat.roll_no == roll_no and seat.cancelled == 0:
            session.close()
            raise HTTPException(status_code=400, detail="Ride has already been booked")

    existing_booking = (
        session.query(Seats)
        .join(Rides, Seats.ride_id == Rides.id)
        .filter(
            Seats.roll_no == roll_no,
            Seats.cancelled == 0,
            Rides.ride_date == ride.ride_date,
        )
        .first()
    )
    if existing_booking:
        session.close()
        raise HTTPException(status_code=400, detail="Student has already joined another ride on this date")

    book = Seats(ride_id=ride.id, roll_no=roll_no, booked_on=date.today(), cancelled=0)
    session.add(book)

    ride.seats_left = ride.seats_left - 1
    session.commit()

    response = {
        "id": book.id,
        "ride_id": book.ride_id,
        "roll_no": book.roll_no,
        "booked_on": book.booked_on,
        "cancelled": book.cancelled,
    }
    session.close()
    return response


def get_ride(ride_id):
    session = Session(engine)
    ride = session.query(Rides).filter(Rides.id == ride_id).first()
    if not ride:
        session.close()
        return None

    passengers_no = session.query(Seats).filter(Seats.ride_id == ride.id, Seats.cancelled == 0).all()
    response = [{"roll_no": passenger.roll_no} for passenger in passengers_no]
    session.close()
    return response
