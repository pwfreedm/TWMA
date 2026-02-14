from db import *
from forms import *
cl = Client(
    name="Test", 
    email="test@gmail.com", 
    phone="7177996491", 
    address="1600 Pennsylvania Ave, DC, Washington DC", 
    mileage=100, 
    travel_thresh=True
)
pa = Patient(name="pt_name", 
             species="pt_spec", 
             sex="M", 
             weight=135, 
             disposal="burial", 
             pawprints=3, 
             age=15, 
             breed="pt_breed", 
             color="color", 
             notes="test animal. disregard")
ap = Appointment(date="1/26/2027", time="never")
vet = Vet(name="coolname", email="email", phone="phone", address="address")


def test_db_schema():
    database = Database("test.db")
    database.add_record(cl, pa, ap, vet)
    print_all(database)

def test_consent_gen(filepath: str):
    con = Consent(cl, pa, ap)
    con.generate("./blanks/Euthanasia_Consent_Jan_2026.pdf", filepath)


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
    test_db_schema()
    test_consent_gen(".")
