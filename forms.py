from pypdf import PdfReader, PdfWriter
from db import Client, Patient, Appointment
from abc import ABC, abstractmethod
import os as os
from pathlib import Path


class GenerableForm(ABC):

    @abstractmethod
    def generate(self):
        """generation fills the form @p blank and stores it in @p filepath"""
        pass

    @abstractmethod
    def _mk_fp (self):
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
    fp: Path = os.path.join(os.path.expanduser('~'), 'Desktop', 'Consents')


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

    def _mk_fp(self) -> Path:
        path = os.path.join(self.fp, str(self._date))
        os.makedirs(path, exist_ok=True)
        return path

    def generate(self):
        reader = PdfReader(stream=Path("blanks/Euthanasia_Consent_Jan_2026.pdf"))
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
        writer.write(os.path.join(self._mk_fp(), f"{self._pet}.pdf"))


