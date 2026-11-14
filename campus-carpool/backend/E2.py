from functions import *


def get_ride(ride_id):
    session = Session(engine)
    ride = session.query(Rides).filter(Rides.id == ride_id).first()
    if not ride:
        session.close()
        return None

    passengers_no = session.query(Seats).filter(
        Seats.ride_id == ride.id,
        Seats.cancelled == 0
    ).all()

    response = [{"roll_no": passenger.roll_no} for passenger in passengers_no]
    session.close()
    return response
