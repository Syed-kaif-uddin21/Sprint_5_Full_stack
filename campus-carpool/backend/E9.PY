from functions import *

def popular_routes():
    session = Session(engine)
    rides = session.query(Rides).filter(Rides.status == "completed").all()
    routes = {}
    for ride in rides:
        route = (ride.from_place, ride.to_place)
        routes[route] = routes.get(route, 0) + 1

    popular = [
        {
            "from_place": route[0],
            "to_place": route[1],
            "total_rides": total
        }
        for route, total in routes.items()
    ]
    popular.sort(key=lambda x: x["total_rides"], reverse=True)
    session.close()
    return popular
