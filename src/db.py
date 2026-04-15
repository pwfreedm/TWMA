import sqlite3 as sq
from typing import List
from pathlib import Path
import os as os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey

from src.utils import address
from src.core import app

class DB_Base (DeclarativeBase):
     metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

db = SQLAlchemy(model_class=DB_Base)

class Client (db.Model, DB_Base):
    __tablename__ = "client"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(31))
    address: Mapped[str] = mapped_column(String(150))
    travel: Mapped[int] = mapped_column(Integer)

    # Relationship definitions for ORM
    animals: Mapped[List["Patient"]] = relationship(back_populates="owner")

class Vet (db.Model, DB_Base):
    __table_name__ = "vet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    comm: Mapped[str] = mapped_column(String)

    # Relationship definitions for ORM
    animals: Mapped[List["Patient"]] = relationship(back_populates="vet")


class Patient (db.Model, DB_Base):
    __tablename__ = "patient"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String[100], nullable=False)
    species: Mapped[str] = mapped_column(String[75])
    sex: Mapped[str] = mapped_column(String[6])
    breed: Mapped[str] = mapped_column(String[50])
    age: Mapped[int] = mapped_column(Integer)
    weight: Mapped[int] = mapped_column(Integer)
    disposal: Mapped[str] = mapped_column(String[10])
    pawprints: Mapped[int] = mapped_column(Integer)
    notes: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(ForeignKey("client.id"))
    vet_id: Mapped[int] = mapped_column(ForeignKey("vet.id"))

    # Relationship definitions for ORM
    owner: Mapped["Client"] = relationship(back_populates="animals")
    appt: Mapped["Appointment"] = relationship(back_populates="patient")
    vet: Mapped["Vet"] = relationship(back_populates="animals")

class Appointment (db.Model, DB_Base):
    __tablename__ = "appointment"
    id: Mapped[int] = mapped_column(ForeignKey("patient.id"), primary_key=True, autoincrement=False)
    date: Mapped[str] = mapped_column(String[15])
    time: Mapped[str] = mapped_column(String[10])

    # Relationship definitions for ORM
    patient: Mapped["Patient"] = relationship(back_populates="appt", single_parent=True)

def register_pt (data:  map[str, str]):
    data = {k : v.lower() for k, v in data.items()}
    client = Client(name=data['client'], 
                email=data['email'], 
                phone=data['phone'], 
                address=address(data['address'], data['city'], data['state'], data['zip']),
                travel=data['travel']
                )
    patient = Patient(name=data['patient'],
                species=data['animal'],
                sex=data['sex'],
                breed=data['breed'],
                age=data['age'],
                weight=data['weight'],
                disposal=data['disposal'],
                pawprints=data['prints'],
                notes=data['notes']
                )
    appt = Appointment(date=data['date'], 
                    time=data['time']
                    )
    vet = Vet(name=data['vet'], comm='')

    #defining relationships
    #TODO: add a get_if_exists and get the client and vet if they already exist.
    client.animals += [patient]
    vet.animals += [patient]
    patient.owner = client
    patient.appt = appt
    patient.vet = vet
    appt.patient = patient

    with app.app_context():
        db.session.add_all([client, vet, patient, appt])
        db.session.commit()