from functions import *

def get_rides(from_location=None, to_location=None, date=None):
    session = Session(engine)
    query = session.query(Rides)

    if from_location:
        query = query.filter(Rides.from_place == from_location)
    if to_location:
        query = query.filter(Rides.to_place == to_location)
    if date:
        query = query.filter(Rides.ride_date == date)

    rides = query.all()
    session.close()
    return rides
