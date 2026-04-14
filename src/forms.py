from pypdf import PdfReader, PdfWriter
from abc import ABC, abstractmethod
import os as os
from enum import Enum
from pathlib import Path
from datetime import date

from src.utils import address

class FormType(Enum):
    CONSENT = 1

class Form (ABC):
    _writer: PdfWriter

    def __init__ (self, wr: PdfWriter):
        self._writer = wr
            
    @abstractmethod
    def save (self, fp: str | Path):
        raise NotImplementedError("Must implement a save method for this form.")

class ConsentForm(Form):

    def __init__ (self, wr: PdfWriter):
        super().__init__(wr)

    def save (self, fp: str | Path = os.path.join(os.path.expanduser('~'), 'Desktop', 'Consents')):
        """ Saves this consent form. 
            The default path to which a consent will be saved is:
            ~/Desktop/Consents/Appt_Date/Last_Name.pdf
        """        
        form = self._writer.get_form_text_fields()
        lastname = form['owner'].split(" ")[-1]

        path: str = os.path.join(fp, str(form['date']))
        os.makedirs(path, exist_ok=True)

        self._writer.remove_annotations(subtypes='/Widget')
        self._writer.write(os.path.join(path, f"{lastname}.pdf"))
        
class FormFactory():
    _data: dict

    def __init__ (self, data: dict):
        self._data = data
    
    def generate(self, type: FormType):
        """NOTE: Generation does not remove annotations. Remove annotaions immediately before writing output."""
        match type:
            case FormType.CONSENT:
                return self._generate_consent()
    
    def _get_date_time(self):
        #TODO: fix this. Currently it always returns 12 AM as the time
        #TODO: day, month, year instead of year, month, date.
        #good job AI, did everything wrong here.
        if self._data['date'] and self._data['time']:
            time = date.strptime(self._data['time'], "%H:%M")
            return  time.strftime("%I:%M %p") + ' ' + self._data['date']
        return None
    
    def get_elem(self, name: str):
        return str(self._data[name]).title()
    
    def _generate_consent(self):
        reader = PdfReader(stream=Path("blanks/Euthanasia_Consent.pdf"))
        writer = PdfWriter()

        writer.append(reader)
        writer.update_page_form_field_values(
            writer.pages[0],
            {
                "date": self.get_elem('date'),
                "owner": self.get_elem('client'),
                "address": address(self._data['address'], self._data['city'], self._data['state'], self._data['zip']),
                "phone": self.get_elem('phone'),
                "pet": self.get_elem('patient'),
                "breed": self.get_elem('breed'),
                "species": self.get_elem('animal'),
                "sex": self.get_elem('sex'),
                "age": self.get_elem('age'),
                "weight": self.get_elem('weight'),
                "email": self._data['email'],
                "vet": self.get_elem('vet'),
                "appt": self._get_date_time(),
                "disposal": self.get_elem('disposal'),
                "fee": self.get_elem('travel')
            },
            auto_regenerate=False, 
            flatten=True
        )
        return ConsentForm(writer)
        
