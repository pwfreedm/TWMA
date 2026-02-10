from db import *


def test():
    database = Database("test.db")
    cl = Client(
        "Test", "7177996491", "1600 Pennsylvania Ave, DC, Washington DC", 100, 1
    )
    pa = Patient("name", "species", "gender", 100, "disposal", 2)
    ap = Appointment("today", "never")
    vet = Vet("coolname", "email", "phone", "address")
    database.add_record(cl, pa, ap, vet)
    print_all(database)


def print_all(database: Database):
    q1 = "SELECT * FROM Patients"
    q2 = "SELECT * FROM Appointments"
    q3 = "SELECT * FROM Clients"
    q4 = "SELECT * FROM Vets"
    r1 = database._cursor.execute(q1).fetchall()
    r2 = database._cursor.execute(q2).fetchall()
    r3 = database._cursor.execute(q3).fetchall()
    r4 = database._cursor.execute(q4).fetchall()
    print(r1)
    print("-----------------------------------------------------------")
    print(r2)
    print("-----------------------------------------------------------")
    print(r3)
    print("-----------------------------------------------------------")
    print(r4)


if __name__ == "__main__":
    test()
