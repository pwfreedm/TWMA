from queue import Queue

forms: Queue[dict] = Queue(maxsize=10)

def enqueue (form: dict[str,str]) -> int:
   global forms
   forms.put(form)


def dequeue () -> dict[str,str]:
   global forms
   return forms.get()

def address (street: str, city: str, state: str, zip: str) -> str: 
   return street + ', ' + city + ', ' + state + ' ' + zip if len(street) > 0 else ""