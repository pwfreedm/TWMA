import sqlite3 as sq
from typing import List
from pathlib import Path
import os as os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    sex: Mapped[bool] = mapped_column(String[6])
    breed: Mapped[str] = mapped_column(String[50])
    age: Mapped[int] = mapped_column(Integer)
    weight: Mapped[int] = mapped_column(Integer)
    disposal: Mapped[str] = mapped_column(String[10])
    pawprints: Mapped[int] = mapped_column(Integer)
    notes: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(ForeignKey("client.id"))

    # Relationship definitions for ORM
    owner: Mapped["Client"] = relationship(back_populates="animals")
    appt: Mapped["Appointment"] = relationship(back_populates="patient")
    vet: Mapped["Vet"] = relationship(back_populates="animals")

class Appointment (db.Model, DB_Base):
    __tablename__ = "appointment"
    id: Mapped[int] = mapped_column(ForeignKey("patient.id"), primary_key=True, autoincrement=False)
    date: Mapped[str] = mapped_column(String[15], nullable=False)
    time: Mapped[str] = mapped_column(String[10], nullable=False)

    # Relationship definitions for ORM
    patient: Mapped["Patient"] = relationship(back_populates="appt", single_parent=True)


# class Database:
#     _connection: sq.Connection
#     _cursor: sq.Cursor

#     def __init__(self, path: Path = Path(os.path.join(os.path.expanduser('~'), 'Documents', 'TWMA_DB'))):
#         db_exists: bool = path.is_dir()
#         if not db_exists:
#             os.makedirs(path, exist_ok= True)
#         self._connection = sq.connect(os.path.join(path, 'TWMA.db'))
#         self._cursor = self._connection.cursor()
#         if not db_exists:
#             self.__setup()

#     def __setup(self):
#         self._connection.execute("PRAGMA foreign_keys = ON")
#         self._cursor.execute(
#             """CREATE TABLE Clients(
#                     id INTEGER PRIMARY KEY,
#                     name TEXT NOT NULL,
#                     email TEXT,
#                     phone TEXT,
#                     address TEXT
#                     )"""
#         )
#         self._cursor.execute(
#             """CREATE TABLE Vets(
#                     id INTEGER PRIMARY KEY,
#                     name TEXT NOT NULL,
#                     contact TEXT
#                     )"""
#         )
#         self._cursor.execute(
#             """CREATE TABLE Patients(
#                     id INTEGER PRIMARY KEY,
#                     name TEXT NOT NULL,
#                     species TEXT,
#                     sex TEXT,
#                     breed TEXT,
#                     age INTEGER,
#                     weight INTEGER,
#                     color TEXT,
#                     disposal TEXT,
#                     pawprints INTEGER,
#                     notes TEXT,
#                     vet_ID INTEGER REFERENCES Vets(id),
#                     owner_ID INTEGER NOT NULL REFERENCES Clients(id)
#                     )"""
#         )
#         self._cursor.execute(
#             """CREATE TABLE Appointments(
#                     id INTEGER PRIMARY KEY REFERENCES Patients(id),
#                     date TEXT NOT NULL,
#                     time TEXT NOT NULL,
#                     owner_ID INTEGER NOT NULL REFERENCES Clients(id)
#                     )"""
#         )
#         self._connection.commit()

#     def valid_table_name(self, table_name: str) -> bool:
#         query = "SELECT 1 FROM sqlite_master WHERE type='table' and name=?"
#         return self._cursor.execute(query, (table_name,)).fetchone() is not None

#     def count_rows(self, table_name: str) -> int | None:
#         if self.valid_table_name(table_name):
#             query = "SELECT COUNT(*) FROM {}".format(table_name)
#             return self._cursor.execute(query).fetchone()[0]
#         return None

#     def get_vet_id(self, vet):
#         query = "SELECT id FROM Vets WHERE name=?"
#         res = self._cursor.execute(query, (vet._name,)).fetchone()
#         rows = self.count_rows("Vets")
#         return (res[0] if res else rows, rows)

#     def add_record(self, client: Client, patient: Patient, appt: Appointment, vet: Vet):
#         client_id = self.count_rows("Clients")
#         patient_id = self.count_rows("Patients")
#         (vet_id, vet_row_count) = self.get_vet_id(vet)

#         self._cursor.execute(
#             "INSERT INTO Clients VALUES(?, ?, ?, ?, ?)",
#             client.generate_sql_value(client_id),
#         )
#         if vet_id == vet_row_count:
#             self._cursor.execute(
#                 "INSERT INTO Vets VALUES(?, ?, ?)", vet.generate_sql_value(vet_id)
#             )
#         self._cursor.execute(
#             "INSERT INTO Patients VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
#             patient.generate_sql_value(patient_id, client_id, vet_id),
#         )
#         self._cursor.execute(
#             "INSERT INTO Appointments VALUES(?, ?, ?, ?)",
#             appt.generate_sql_value(client_id, patient_id),
#         )
#         self._connection.commit()
