import os
from sqlalchemy import Integer, String, Column, create_engine, ForeignKey, DateTime, Date, Time
from sqlalchemy.orm import declarative_base, Session
from datetime import date, timedelta, timezone, datetime
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "carpool.db")
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Rides(Base):
    __tablename__ = "rides"
    id = Column(Integer, primary_key=True)
    driver_roll = Column(String)
    from_place = Column(String)
    to_place = Column(String)
    ride_date = Column(Date, default=date.today)
    depart_time = Column(Time)
    total_seats = Column(Integer)
    seats_left = Column(Integer)
    status = Column(String)


class Seats(Base):
    __tablename__ = "seats"
    id = Column(Integer, primary_key=True)
    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=False)
    roll_no = Column(String, nullable=False)
    booked_on = Column(DateTime, default=date.today)
    cancelled = Column(Integer, nullable=False, default=0)

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    role = Column(String, default="user")


Base.metadata.create_all(engine)

ACCESS_TOKEN_EXPIRY = 10
REFRESH_TOKEN_EXPIRY = 7 * 24 * 60
SECRET_KEY = "hbsdkkfhjbiiss"
ALGORITHM = "HS256"
ph = PasswordHasher()


def verify_login(username, password):
    session = Session(engine)
    user = session.query(User).filter(User.username == username).first()
    if not user:
        session.close()
        return False
    try:
        ph.verify(user.password, password)
    except VerifyMismatchError:
        session.close()
        return False

    user_role = user.role
    session.close()
    access_token = create_token(username=username, role=user_role, token_type="access")
    refresh_token = create_token(username=username, role=user_role, token_type="refresh")
    return {"access_token": access_token, "refresh_token": refresh_token}


def create_token(username, token_type, role):
    time = ACCESS_TOKEN_EXPIRY
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload = {
        "username": username,
        "role": role,
        "token_type": token_type,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=time),
    }
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token, token_type):
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None
    if payload.get("token_type") == token_type:
        return {
            "username": payload["username"],
            "role": payload.get("role", "user")
        }
    return None


def register_user(username, password, role="user"):
    session = Session(engine)
    user_exist = session.query(User).filter(User.username == username).first()
    if user_exist is not None:
        session.close()
        return False
    session.add(User(username=username, password=ph.hash(password), role=role))
    session.commit()
    session.close()
    return True