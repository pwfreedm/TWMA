
def address (street: str, city: str, state: str, zip: str) -> str: 
   return street + ', ' + city + ', ' + state + ' ' + zip if len(street) > 0 else ""
