from datetime import date, datetime, timedelta, timezone
from sqlalchemy import Column, Integer, String, Float, Date, create_engine, ForeignKey
from sqlalchemy.orm import Session, declarative_base, session
from fastapi import HTTPException
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

DB_PATH = "warehouse.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Package(Base):
    __tablename__ = "packages"
    id = Column(Integer, primary_key=True)
    package_name = Column(String)
    destination = Column(String)
    weight = Column(Float)
    arrival_date = Column(Date, default=date.today)
    status = Column(String)
    batch_id = Column(Integer, ForeignKey("dispatch_batches.id"))

class DispatchBatches(Base):
    __tablename__ = "dispatch_batches"
    id = Column(Integer, primary_key=True)
    batch_number = Column(String)
    destination = Column(String)
    vehicle = Column(String)
    dispatch_date = Column(Date, default=date.today)
    dispatch_status = Column(String)

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    role = Column(String, default="user")

Base.metadata.create_all(engine)


def register_package(name, destination, weight, status):

    session = Session(engine)
    item = Package(package_name=name, destination=destination, weight=weight, status=status)
    session.add(item)
    session.commit()

def get_registration():
    session = Session(engine)
    item = session.query(Package).all()
    return item

def get_specific_package(package_id):
    session = Session(engine)
    item = session.query(Package).filter(Package.id == package_id).first()
    return item

def update_package(package_id, weight, destination, status):
    session = Session(engine)
    item = session.query(Package).filter(Package.id == package_id).first()
    item.weight = weight
    item.destination = destination
    item.status = status

    session.commit()
    session.close()


def delete_specific_package(package_id):
    session = Session(engine)
    item = session.query(Package).filter(Package.id == package_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Package not found")

    if item.status != "dispatched":
        session.delete(item)

    session.commit()
    session.close()


def filter_package(destination=None, status=None, arrival_date=None):
    session = Session(engine)
    query = session.query(Package)

    if destination:
        query = query.filter(Package.destination == destination)
    if status:
        query = query.filter(Package.status == status)
    if arrival_date:
        query = query.filter(Package.arrival_date == arrival_date)

    item = query.all()
    session.close()
    return item


def filter_batch(destination=None, vehicle=None, dispatch_status=None):
    session = Session(engine)
    query = session.query(DispatchBatches)

    if destination:
        query = query.filter(DispatchBatches.destination == destination)
    if vehicle:
        query = query.filter(DispatchBatches.vehicle == vehicle)
    if dispatch_status:
        query = query.filter(DispatchBatches.dispatch_status == dispatch_status)

    item = query.all()
    session.close()
    return item

def dispatch_summary():
    session = Session(engine)
    query_count = session.query(Package).count()
    query_pending = session.query(Package).filter(Package.status == "pending").count()
    query_dispatched = session.query(Package).filter(Package.status == "dispatched").count()
    query_destination_count = session.query(Package).group_by(Package.destination).count()

    response = {
        "query_count": query_count,
        "query_pending": query_pending,
        "query_dispatched": query_dispatched,
        "query_destination_count": query_destination_count
    }

    return response


def add_package(packages):
    session = Session(engine)

    for package in packages:
        response = Package(
            package_name=package["package_name"],
            destination=package["destination"],
            weight=package["weight"],
            arrival_date=date.fromisoformat(package["arrival_date"]),
            status=package["status"],
            batch_id=int(package["batch_id"]) if package.get("batch_id") else None
        )
        session.add(response)

    print("added packages")
    session.commit()
    session.close()

def add_batches(batches):
    session = Session(engine)

    for batch in batches:
        response = DispatchBatches(
            batch_number=batch["batch_number"],
            destination=batch["destination"],
            vehicle=batch["vehicle"],
            dispatch_date=date.fromisoformat(batch["dispatch_date"]),
            dispatch_status=batch["dispatch_status"]
        )
        session.add(response)

    print("added batches")
    session.commit()
    session.close()

packages = [
  {
    "id": 1,
    "package_name": "Electronics Box",
    "destination": "Bangalore",
    "weight": 12.5,
    "arrival_date": "2026-11-01",
    "status": "dispatched",
    "batch_id": "1"
  },
  {
    "id": 2,
    "package_name": "Office Furniture",
    "destination": "Mysore",
    "weight": 45.0,
    "arrival_date": "2026-11-02",
    "status": "pending",
    "batch_id": "2"
  },
  {
    "id": 3,
    "package_name": "Clothing Carton",
    "destination": "Chennai",
    "weight": 8.2,
    "arrival_date": "2026-11-02",
    "status": "in_transit",
    "batch_id": "3"
  },
  {
    "id": 4,
    "package_name": "Kitchen Appliances",
    "destination": "Hyderabad",
    "weight": 23.7,
    "arrival_date": "2026-11-03",
    "status": "pending",
    "batch_id": "4"
  },
  {
    "id": 5,
    "package_name": "Books Shipment",
    "destination": "Mumbai",
    "weight": 15.4,
    "arrival_date": "2026-11-03",
    "status": "dispatched",
    "batch_id": "5"
  },
  {
    "id": 6,
    "package_name": "Sports Equipment",
    "destination": "Pune",
    "weight": 32.8,
    "arrival_date": "2026-11-04",
    "status": "pending",
    "batch_id": "6"
  },
  {
    "id": 7,
    "package_name": "Medical Supplies",
    "destination": "Delhi",
    "weight": 18.6,
    "arrival_date": "2026-11-04",
    "status": "dispatched",
    "batch_id": "7"
  },
  {
    "id": 8,
    "package_name": "Computer Parts",
    "destination": "Kochi",
    "weight": 9.3,
    "arrival_date": "2026-11-05",
    "status": "in_transit",
    "batch_id": "8"
  },
  {
    "id": 9,
    "package_name": "Industrial Tools",
    "destination": "Bangalore",
    "weight": 56.2,
    "arrival_date": "2026-11-05",
    "status": "pending",
    "batch_id": "9"
  },
  {
    "id": 10,
    "package_name": "Mobile Accessories",
    "destination": "Mysore",
    "weight": 6.5,
    "arrival_date": "2026-11-06",
    "status": "dispatched",
    "batch_id": "10"
  },
  {
    "id": 11,
    "package_name": "Automobile Parts",
    "destination": "Chennai",
    "weight": 41.9,
    "arrival_date": "2026-11-06",
    "status": "pending",
    "batch_id": "11"
  },
  {
    "id": 12,
    "package_name": "Packaging Materials",
    "destination": "Hyderabad",
    "weight": 27.3,
    "arrival_date": "2026-11-07",
    "status": "in_transit",
    "batch_id": "12"
  }
]

batches = [
  {
    "id": 1,
    "batch_number": "BATCH-1001",
    "destination": "Bangalore",
    "vehicle": "101",
    "dispatch_date": "2026-11-08",
    "dispatch_status": "completed"
  },
  {
    "id": 2,
    "batch_number": "BATCH-1002",
    "destination": "Mysore",
    "vehicle": "102",
    "dispatch_date": "2026-11-09",
    "dispatch_status": "pending"
  },
  {
    "id": 3,
    "batch_number": "BATCH-1003",
    "destination": "Chennai",
    "vehicle": "103",
    "dispatch_date": "2026-11-09",
    "dispatch_status": "in_transit"
  },
  {
    "id": 4,
    "batch_number": "BATCH-1004",
    "destination": "Hyderabad",
    "vehicle": "104",
    "dispatch_date": "2026-11-10",
    "dispatch_status": "pending"
  },
  {
    "id": 5,
    "batch_number": "BATCH-1005",
    "destination": "Mumbai",
    "vehicle": "105",
    "dispatch_date": "2026-11-10",
    "dispatch_status": "completed"
  },
  {
    "id": 6,
    "batch_number": "BATCH-1006",
    "destination": "Pune",
    "vehicle": "106",
    "dispatch_date": "2026-11-11",
    "dispatch_status": "pending"
  },
  {
    "id": 7,
    "batch_number": "BATCH-1007",
    "destination": "Delhi",
    "vehicle": "107",
    "dispatch_date": "2026-11-11",
    "dispatch_status": "completed"
  },
  {
    "id": 8,
    "batch_number": "BATCH-1008",
    "destination": "Kochi",
    "vehicle": "108",
    "dispatch_date": "2026-11-12",
    "dispatch_status": "in_transit"
  },
  {
    "id": 9,
    "batch_number": "BATCH-1009",
    "destination": "Bangalore",
    "vehicle": "109",
    "dispatch_date": "2026-11-12",
    "dispatch_status": "pending"
  },
  {
    "id": 10,
    "batch_number": "BATCH-1010",
    "destination": "Mysore",
    "vehicle": "110",
    "dispatch_date": "2026-11-13",
    "dispatch_status": "completed"
  },
  {
    "id": 11,
    "batch_number": "BATCH-1011",
    "destination": "Chennai",
    "vehicle": "111",
    "dispatch_date": "2026-11-13",
    "dispatch_status": "pending"
  },
  {
    "id": 12,
    "batch_number": "BATCH-1012",
    "destination": "Hyderabad",
    "vehicle": "112",
    "dispatch_date": "2026-11-14",
    "dispatch_status": "in_transit"
  }
]

USER_NAME = "Kaif"
PASSWORD = "12345"

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

if __name__ == "__main__":
    add_batches(batches)
    add_package(packages)