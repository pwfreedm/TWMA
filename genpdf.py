from src.forms import FormFactory, FormType
import subprocess

data = {
    "date": "test",
    "client": "Peter Freedman",
    "address": "307 Winding Hill Drive",
    "city": "Lancaster",
    "state": "PA",
    "zip": "17601",
    "phone": "717-799-6491",
    "patient": "Sam",
    "animal": "Dog",
    "breed": "Husky Mix",
    "sex": "Male",
    "age": "14",
    "weight": "40",
    "email": "frdmanp@gmail.com",
    "vet": "Mark Huber",
    "date": "2024-10-10",
    "time": "15:50",
    "disposal": "home",
    "travel": "55",
    "prints": "33"
}

f = FormFactory(data)
con = f.generate(FormType.CONSENT)
con.save("./")
bom = f.generate(FormType.BILL_OF_MATERIALS)
bom.save("./")