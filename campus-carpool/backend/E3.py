from functions import *

def offer_ride(driver_roll, from_place , to_place, ride_date, depart_time , total_seats) :
    session=Session(engine)
    new_ride = Rides(
        driver_roll=driver_roll,
        from_place=from_place,
        to_place=to_place,
        ride_date=ride_date,
        depart_time=depart_time,
        total_seats=total_seats,
        seats_left=total_seats,
        status="scheduled"
    )
    session.add(new_ride)
    session.commit()

    response = {
        "id": new_ride.id,  
        "driver_roll": new_ride.driver_roll,
        "from_place": new_ride.from_place,
        "to_place": new_ride.to_place,
        "ride_date": new_ride.ride_date,
        "depart_time": new_ride.depart_time,
        "total_seats": new_ride.total_seats,
        "seats_left": new_ride.seats_left,
        "status": new_ride.status

    }
    session.close()

    return response
