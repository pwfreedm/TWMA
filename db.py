import sqlite3 as sq
from pathlib import Path
import os as os

class Client:
    _name: str
    _email: str
    _phone: str
    _address: str
    _mileage: int
    _travel: int

    def __init__(
        self,
        name: str,
        email: str,
        phone: str,
        address: str,
        mileage: int,
        travel_thresh: int = 0,
    ):
        self._name = name
        self._phone = phone
        self._address = address
        self._email = email
        self._mileage = mileage
        self._travel = 0

    def generate_sql_value(self, id: int):
        return (
            id,
            self._name,
            self._email,
            self._phone,
            self._address,
            self._mileage,
            self._travel,
        )

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def phone(self):
        return self._phone

    @property
    def address(self):
        return self._address

    @property
    def mileage(self):
        return self._mileage

    @property
    def travel(self):
        return self._travel


class Patient:
    _name: str
    _species: str
    _sex: str
    _breed: str
    _age: int
    _weight: int
    _color: str
    _disposal: str
    _pawprints: int
    _notes: str

    def __init__(
        self,
        name: str,
        species: str,
        sex: str,
        weight: int,
        disposal: str,
        pawprints: int,
        age: int,
        breed: str = "",
        color: str = "",
        notes: str = "",
    ):
        self._name = name
        self._species = species
        self._sex = sex
        self._breed = breed
        self._age = age
        self._weight = weight
        self._color = color
        self._disposal = disposal
        self._pawprints = pawprints
        self._notes = notes

    def generate_sql_value(self, id: int, owner_ID: int, vet_ID: int):
        return (
            id,
            self._name,
            self._species,
            self._sex,
            self._breed,
            self._age,
            self._weight,
            self._color,
            self._disposal,
            self._pawprints,
            self._notes,
            vet_ID,
            owner_ID,
        )

    @property
    def name(self):
        return self._name

    @property
    def species(self):
        return self._species

    @property
    def sex(self):
        return self._sex

    @property
    def breed(self):
        return self._breed

    @property
    def age(self):
        return self._age

    @property
    def weight(self):
        return self._weight

    @property
    def color(self):
        return self._color

    @property
    def disposal(self):
        return self._disposal

    @property
    def pawprints(self):
        return self._pawprints

    @property
    def notes(self):
        return self._notes


class Appointment:
    _date: str
    _time: str

    def __init__(self, date: str, time: str):
        self._date = date
        self._time = time

    def generate_sql_value(self, owner_ID: int, patient_ID: int):
        return (patient_ID, self._date, self._time, owner_ID)

    @property
    def date(self):
        return self._date

    @property
    def time(self):
        return self._time


class Vet:
    _name: str
    _email: str
    _phone: str
    _address: str

    def __init__(self, name: str, email: str, phone: str = "", address: str = ""):
        self._name = name
        self._email = email
        self._phone = phone
        self._address = address

    def generate_sql_value(self, id: int):
        return (id, self._name, self._email, self._phone, self._address)

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def phone(self):
        return self._phone

    @property
    def address(self):
        return self._address


class Database:
    _connection: sq.Connection
    _cursor: sq.Cursor

    def __init__(self, path: Path = Path(os.path.join(os.path.expanduser('~'), 'Documents', 'TWMA_DB'))):
        db_exists: bool = path.is_dir()
        if not db_exists:
            os.makedirs(path, exist_ok= True)
        self._connection = sq.connect(os.path.join(path, 'TWMA.db'))
        self._cursor = self._connection.cursor()
        if not db_exists:
            self.__setup()

    def __setup(self):
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._cursor.execute(
            """CREATE TABLE Clients(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    address TEXT NOT NULL,
                    travel_time INTEGER,
                    travel_fee INTEGER
                    )"""
        )
        self._cursor.execute(
            """CREATE TABLE Vets(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT,
                    address TEXT
                    )"""
        )
        self._cursor.execute(
            """CREATE TABLE Patients(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    species TEXT NOT NULL,
                    sex TEXT NOT NULL,
                    breed TEXT,
                    age INTEGER NOT NULL,
                    weight INTEGER NOT NULL,
                    color TEXT,
                    disposal TEXT NOT NULL,
                    pawprints INTEGER NOT NULL,
                    notes TEXT NOT NULL,
                    vet_ID INTEGER NOT NULL REFERENCES Vets(id),
                    owner_ID INTEGER NOT NULL REFERENCES Clients(id)
                    )"""
        )
        self._cursor.execute(
            """CREATE TABLE Appointments(
                    id INTEGER PRIMARY KEY REFERENCES Patients(id),
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    owner_ID INTEGER NOT NULL REFERENCES Clients(id)
                    )"""
        )
        self._connection.commit()

    def valid_table_name(self, table_name: str) -> bool:
        query = "SELECT 1 FROM sqlite_master WHERE type='table' and name=?"
        return self._cursor.execute(query, (table_name,)).fetchone() is not None

    def count_rows(self, table_name: str) -> int | None:
        if self.valid_table_name(table_name):
            query = "SELECT COUNT(*) FROM {}".format(table_name)
            return self._cursor.execute(query).fetchone()[0]
        return None

    def get_vet_id(self, vet):
        query = "SELECT id FROM Vets WHERE name=?"
        res = self._cursor.execute(query, (vet._name,)).fetchone()
        rows = self.count_rows("Vets")
        return (res[0] if res else rows, rows)

    def add_record(self, client: Client, patient: Patient, appt: Appointment, vet: Vet):
        client_id = self.count_rows("Clients")
        patient_id = self.count_rows("Patients")
        (vet_id, vet_row_count) = self.get_vet_id(vet)

        self._cursor.execute(
            "INSERT INTO Clients VALUES(?, ?, ?, ?, ?, ?, ?)",
            client.generate_sql_value(client_id),
        )
        if vet_id == vet_row_count:
            self._cursor.execute(
                "INSERT INTO Vets VALUES(?, ?, ?, ?, ?)", vet.generate_sql_value(vet_id)
            )
        self._cursor.execute(
            "INSERT INTO Patients VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            patient.generate_sql_value(patient_id, client_id, vet_id),
        )
        self._cursor.execute(
            "INSERT INTO Appointments VALUES(?, ?, ?, ?)",
            appt.generate_sql_value(client_id, patient_id),
        )
        self._connection.commit()
