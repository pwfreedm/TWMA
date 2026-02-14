from pypdf import PdfReader, PdfWriter
from db import Client, Patient, Appointment
from abc import ABC, abstractmethod
from re import sub
from os import makedirs

bad_fp_chars: str = r'[<>:"/\\|?*]'

class GenerableForm(ABC):

    @abstractmethod
    def generate(self, blank: str, filepath: str):
        """generation fills the form @p blank and stores it in @p filepath"""
        pass

    @abstractmethod
    def _mk_fp (self, filepath: str):
        """Makes sure that a correctly formatted filepath exists for the generated form to exist in"""
        pass


class Consent(GenerableForm):
    _date: str
    _owner: str
    _addr: str
    _phone: str
    _pet: str
    _breed: str
    _species: str
    _sex: str
    _age: int
    _color: str
    _email: str

    def __init__(self, client: Client, pt: Patient, appt: Appointment):
        self._date = appt.date
        self._owner = client.name
        self._addr = client.address
        self._phone = client.phone
        self._pet = pt.name
        self._breed = pt.breed
        self._species = pt.species
        self._sex = pt.sex
        self._age = pt.age
        self._color = pt.color
        self._email = client.email

    def _mk_fp(self, filepath: str) -> str:
        path = filepath + f"/{sub(bad_fp_chars,' ', self._date)}/consents"
        makedirs(path, exist_ok=True)
        return path + "/"

    def generate(self, blank: str, filepath: str):
        reader = PdfReader(blank)
        writer = PdfWriter()

        writer.append(reader)
        # flatten = true and remove_annotations remove the pdf elements from the generated output
        writer.update_page_form_field_values(
            writer.pages[0],
            {
                "date": self._date,
                "owner": self._owner,
                "address": self._addr,
                "phone": self._phone,
                "pet": self._pet,
                "breed": self._breed,
                "species": self._species,
                "sex": self._sex,
                "age": self._age,
                "color": self._color,
                "email": self._email
            },
            auto_regenerate=False,
            flatten=True,
        )
        writer.remove_annotations(subtypes="/Widget")
        
        writer.write(self._mk_fp(filepath) + f"{self._pet}.pdf")


