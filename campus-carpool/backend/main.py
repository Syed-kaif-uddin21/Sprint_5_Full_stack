from datetime import date, time
from typing import Optional
from fastapi import FastAPI, HTTPException, Header, Body
from fastapi.middleware.cors import CORSMiddleware
import functions
import E1
import E2
import E3
import E4
import E5
import E6
import E7
import E8
import E9

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- E1: Get upcoming / filtered rides ---
@app.get("/get_rides")
@app.get("/Rides")
def get_rides(
    from_location: Optional[str] = None,
    to_location: Optional[str] = None,
    date: Optional[str] = None,
    from_place: Optional[str] = None,
    to_place: Optional[str] = None,
    ride_date: Optional[str] = None,
    token = Header(None)
):
    username = functions.verify_token(token, "access")
    if not username:
        raise HTTPException(status_code=401)
    from_val = from_location or from_place
    to_val = to_location or to_place
    date_val = date or ride_date
    return E1.get_rides(from_location=from_val, to_location=to_val, date=date_val)

# --- E2: Get one ride by ID with passengers ---
@app.get("/get_ride")
def get_ride(ride_id: Optional[int] = None, id: Optional[int] = None):
    target_id = ride_id if ride_id is not None else id
    if target_id is None:
        raise HTTPException(status_code=422, detail="Ride id is required")
    res = E2.get_ride(ride_id=target_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Ride not found")
    return res

# --- E3: Offer a ride ---
@app.post("/offer_ride")
def offer_ride(driver_roll: str, from_place: str, to_place: str, ride_date: date, depart_time: time, total_seats: int):
    return E3.offer_ride(driver_roll=driver_roll, from_place=from_place, to_place=to_place, ride_date=ride_date, depart_time=depart_time, total_seats=total_seats)

# --- E4: Cancel a ride ---
@app.patch("/cancel")
def cancel(ride_id: int, driver_roll: str):
    return E4.cancel_ride(ride_id, driver_roll)

# --- E5: Join a ride ---
@app.post("/book_ride")
def book_ride(ride_id: int, roll_no: str):
    if ride_id < 1:
        raise HTTPException(status_code=400, detail="Ride id must be greater than 0")
    return E5.join_ride(ride_id, roll_no)

# --- E6: Leave a ride ---
@app.patch("/ride")
def leave_ride(ride_id: int, roll_no: str):
    if ride_id < 1:
        raise HTTPException(status_code=400, detail="Ride id must be greater than 0")
    return E6.leave_ride(ride_id, roll_no)

# --- E7: Mark a ride completed ---
@app.patch("/complete_ride")
def complete_ride(driver_roll: str, ride_id: int):
    return E7.complete_ride(driver_roll, ride_id)

# --- E8: Get a student's rides ---
@app.get("/student_rides")
def student_rides(roll_no: str):
    return E8.student_rides(roll_no)

# --- E9: Get popular routes ---
@app.get("/popular_routes")
def popular_routes():
    return E9.popular_routes()

@app.post("/login")
def login(username=Body(), password=Body()):
    token = functions.verify_login(username=username, password=password)
    if not token:
        raise HTTPException(status_code=401)
    return {"token" : token}

@app.post("/refresh")
def refresh(refresh_token):
    username = functions.verify_token(token=refresh_token,token_type="refresh")
    if not username:
        raise HTTPException(status_code=401, detail="token is invalid")

    access_token = functions.create_token(username=username,token_type="access")
    return {"access_token" : access_token}

@app.post("/register_user")
def register_user(username = Body(), password = Body(), role = Body("user")):
    if functions.register_user(username=username, password=password, role=role):
        return {"message": "user registration successful"}
    raise HTTPException(status_code=400, detail="User already exists")