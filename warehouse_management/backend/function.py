from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Float, Date, create_engine
from sqlalchemy.orm import Session, declarative_base
from fastapi import HTTPException

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