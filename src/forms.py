from pypdf import PdfReader, PdfWriter
from abc import ABC, abstractmethod
import os as os
from enum import Enum
from pathlib import Path

from src.utils import address, wrap_path

class FormType(Enum):
    CONSENT = 1
    BILL_OF_MATERIALS = 2

class Form (ABC):
    _writer: PdfWriter

    def __init__ (self, wr: PdfWriter):
        self._writer = wr
            
    @abstractmethod
    def save (self, fp: str | Path):
        raise NotImplementedError("Must implement a save method for this form.")

class BillOfMaterials(Form):
    def __init__(self, wr: PdfWriter):
        super().__init__(wr)

    def calc_drugs(self):
        data = self._writer.get_form_text_fields()
        [ket, dex, but, euth] = [0,0,0,0]

        weight = int(data['weight'].split(' ')[0])
        species = data['species'].lower()

        if species == 'cat':
            ket = 1
            euth = 1
        elif species == 'dog' and weight <= 30:
            ket = 0.01 * weight - 0.01
            euth = 0.1
        #because we are dealing with drugs, zero everything unless certain it should be more
        elif species == 'dog' and weight > 30:
            but = 0.01 * weight
            euth = 0.1 * weight
            dex = 0.01 * weight - 0.1
        
        self._writer.update_page_form_field_values(
            self._writer.pages[0],
            {
                "ket": f'{ket:.1f}',
                "dex": f'{dex:.1f}',
                "but": f'{but:.1f}',
                "euth": f'{euth:.1f}'
            },
            auto_regenerate=False,
            flatten=True
        )

    def save (self, fp: str | Path = os.path.join(os.path.expanduser('~'), 'Desktop', 'Bill of Materials')):
        """ Saves this Bill of Materials
            The default path to which a BoM will be saved is: 
            ~/Desktop/Bill of Materials/Patient_Name.pdf
        """
        form = self._writer.get_form_text_fields()
        pt_name = ' '.join([form['patient'], form['owner'].split(' ')[-1]])

        self.calc_drugs()

        os.makedirs(fp, exist_ok=True)

        self._writer.remove_annotations(subtypes='/Widget')
        self._writer.write(os.path.join(fp, f'{pt_name}.pdf'))

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
        """NOTE: Generation does not remove annotations. Remove annotaions immediately before writing output.
        
            Annotations will be removed whe a form's save method is called to enable any necessary post-processing
        """
        match type:
            case FormType.CONSENT:
                return self._generate_consent()
            case FormType.BILL_OF_MATERIALS:
                return self._generate_bom()
            
    def _reverse_date(self):
        return '-'.join(self._data['date'].split('-')[::-1])
    
    def _get_date_time(self):
        if self._data['date'] and self._data['time']:
            hrandmin = self._data['time'].split(':')
            time = ':'.join([str(int(hrandmin[0]) % 12), hrandmin[1]])
            amorpm = 'PM' if int(hrandmin[0]) - 12 > 0 else 'AM'
            return  ' '.join([time, amorpm, self._reverse_date()])
        return None
    
    def get_elem(self, name: str):
        return str(self._data[name]).title()
    
    def _generate_bom(self):
        reader = PdfReader(stream=wrap_path(Path("../blanks/Bill_of_Materials.pdf")))
        writer = PdfWriter()

        writer.append(reader)
        writer.update_page_form_field_values(
            writer.pages[0],
            {
                "date": self._reverse_date(),
                "owner": self.get_elem('client'),
                "phone": self._data['phone'],
                "address": address(self._data['address'], self._data['city'], self._data['state'], self._data['zip']),
                "patient": self.get_elem('patient'),
                "species": self.get_elem('animal'),
                "weight": ' '.join([self.get_elem('weight'), 'lbs']),
                "date2": self._reverse_date()
            },
            auto_regenerate=False, 
            flatten=True
        )
        return BillOfMaterials(writer)

    def _generate_consent(self):
        reader = PdfReader(stream=wrap_path(Path("../blanks/Euthanasia_Consent.pdf")))
        writer = PdfWriter()

        writer.append(reader)
        writer.update_page_form_field_values(
            writer.pages[0],
            {
                "date": self._reverse_date(),
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
                "fee": self.get_elem('travel'),
                "prints": self._data['prints']
            },
            auto_regenerate=False, 
            flatten=True
        )
        return ConsentForm(writer)
        
