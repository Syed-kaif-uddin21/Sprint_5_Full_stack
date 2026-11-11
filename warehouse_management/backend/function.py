from sqlalchemy import Integer, String, Column, create_engine, ForeignKey, DateTime
from sqlalchemy.orm import Session, declarative_base
from datetime import date, timedelta
from fastapi import HTTPException

DB_PATH = "lab.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Equipment(Base):
    __tablename__ = "equipment"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    lab_room = Column(String)
    in_service = Column(Integer, default=1)


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    roll_no = Column(String, nullable=False)
    booking_date = Column(String, nullable=False)
    booked_on = Column(DateTime, default=date.today)
    cancelled = Column(Integer, nullable=False, default=0)


Base.metadata.create_all(engine)