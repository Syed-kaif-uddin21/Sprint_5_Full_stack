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