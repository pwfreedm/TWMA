from typing import List
import os as os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, select
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

def find_client (name: str) -> Client|None:
    '''Finds a client, by name, if they are in the DB.
        Returns None if no matches

        NOTE: This method must be called from within an active database session. 
    '''
    query = select(Client).where(Client.name == name.lower())
    return db.session.execute(query).scalar_one_or_none()


def find_vet (name: str) -> Vet|None:
    '''Finds a vet, by name, if they are in the DB.
        Returns None if no matches

        NOTE: This method must be called from within an active database session. 
    '''
    query = select(Vet).where(Vet.name == name.lower())
    return db.session.execute(query).scalar_one_or_none() 

def make_client(data: map[str, str]) -> Client:
    return Client(name=data['client'], 
                email=data['email'], 
                phone=data['phone'], 
                address=address(data['address'], data['city'], data['state'], data['zip']),
                travel=data['travel']
                )

def make_pt (data: str) -> Patient:
    return Patient(name=data['patient'],
                species=data['animal'],
                sex=data['sex'],
                breed=data['breed'],
                age=data['age'],
                weight=data['weight'],
                disposal=data['disposal'],
                pawprints=data['prints'],
                notes=data['notes']
                )

def make_appt (data: str) -> Appointment:
    return Appointment(date=data['date'], 
                    time=data['time']
                    )

def make_vet (data: str) -> Vet:
    comm = ''
    try:
        comm = data['comm']
    except: 
        return Vet(name=data['vet'], comm=comm)

def register_pt (data:  map[str, str]):
    data = {k : v.lower() for k, v in data.items()}

    with app.app_context():

        client = find_client(data['client'])
        if client == None:
            client = make_client(data)

        vet = find_vet(data['vet'])
        if vet == None:
            vet = make_vet(data)

        patient = make_pt(data)
        appt = make_appt(data)

        #defining relationships
        patient.owner = client
        patient.appt = appt
        patient.vet = vet
        appt.patient = patient

        #session needs to be aware of the patient to be able to add it to client and vet lists
        db.session.add(patient)

        #update relationships
        client.animals.append(patient) 
        vet.animals.append(patient)

        db.session.add_all([client, appt, vet])
        db.session.commit()