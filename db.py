import sqlite3 as sq
from pathlib import Path


class Client:
    _name: str
    _phone: str
    _address: str
    _mileage: int
    _travel: int

    def __init__(
        self, name: str, phone: str, address: str, mileage: int, travel_thresh: int = 0
    ):
        self._name = name
        self._phone = phone
        self._address = address
        self._mileage = mileage
        self._travel = 0

    def __generate_sql_value(self, id: int):
        return (id, self._name, self._phone, self._address, self._mileage, self._travel)


class Patient:
    _name: str
    _species: str
    _gender: str
    _breed: str
    _weight: int
    _color: str
    _disposal: str
    _pawprints: int
    _notes: str

    def __init__(
        self,
        name: str,
        species: str,
        gender: str,
        weight: int,
        disposal: str,
        pawprints: int,
        breed: str = "",
        color: str = "",
        notes: str = "",
    ):
        self._name = name
        self._species = species
        self._gender = gender
        self._breed = breed
        self._weight = weight
        self._color = color
        self._disposal = disposal
        self._pawprints = pawprints
        self._notes = notes

    def __generate_sql_value(self, id: int, owner_ID: int, vet_ID: int):
        return (
            id,
            self._name,
            self._species,
            self._gender,
            self._breed,
            self._weight,
            self._color,
            self._disposal,
            self._pawprints,
            self._notes,
            vet_ID,
            owner_ID,
        )


class Appointment:
    _date: str
    _time: str

    def __init__(self, date: str, time: str):
        self._date = date
        self._time = time

    def __generate_sql_value(self, owner_ID: int, patient_ID: int):
        return (patient_ID, self._date, self._time, owner_ID)


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

    def __generate_sql_value(self, id: int):
        return (id, self._name, self._email, self._phone, self._address)


class Database:
    _connection: sq.Connection
    _cursor: sq.Cursor

    def __init__(self, path: str):
        db_exists: bool = Path(path).is_file()
        self._connection = sq.connect(path)
        self._cursor = self._connection.cursor()
        if not db_exists:
            self.__setup()

    def __setup(self):
        self._cursor.execute(
            """CREATE TABLE Clients(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL, 
                    phone TEXT NOT NULL,
                    address TEXT NOT NULL,
                    travel_time INTEGER,
                    travel_fee INTEGER
                    )"""
        )
        self._cursor.execute(
            """CREATE TABLE Patients(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    species TEXT NOT NULL,
                    gender TEXT NOT NULL,
                    breed TEXT,
                    weight INTEGER NOT NULL,
                    color TEXT,
                    disposal TEXT NOT NULL,
                    pawprints INTEGER NOT NULL,
                    notes TEXT NOT NULL
                    vet_ID INTEGER FOREIGN KEY NOT NULL
                    owner_ID INTEGER FOREIGN KEY NOT NULL
                    )"""
        )
        self._cursor.execute(
            """CREATE TABLE Vets(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT,
                    address TEXT,
                    )"""
        )
        self._cursor.execute(
            """CREATE TABLE Appointments(
                    id INTEGER PRIMARY KEY,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    owner_ID INTEGER FOREIGN KEY NOT NULL,
                    )"""
        )

    def count_rows(self, table_name: str) -> int:
        res = self._cursor.execute("SELECT COUNT(*) FROM ?", table_name)
        return res.fetchone()[0]

    def get_vet_id(self, vet):
        res = self._cursor.execute(
            "SELECT id FROM Vets where name=?", vet._name
        ).fetchone()
        return res[0] if res else self.count_rows("Vets")

    def add_record(self, client: Client, patient: Patient, appt: Appointment, vet: Vet):
        client_id = self.count_rows("Clients")
        patient_id = self.count_rows("Patients")
        appt_id = patient_id
        vet_id = self.get_vet_id(vet)

        self._cursor.execute(
            "INSERT INTO Clients VALUES(?)", client.__generate_sql_value(client_id)
        )

        self._cursor.execute(
            "INSERT INTO Patients VALUES(?)",
            patient.__generate_sql_value(patient_id, client_id, vet_id),
        )
        self._cursor.execute(
            "INSERT INTO Appointments VALUES(?)",
            appt.__generate_sql_value(client_id, patient_id),
        )
        self._cursor.execute(
            "INSERT INTO Appointments VALUES(?)", vet.__generate_sql_value(vet_id)
        )
        self._connection.commit()
