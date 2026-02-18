from queue import Queue

forms: Queue[dict] = Queue(maxsize=10)

def enqueue (form: dict[str,str]) -> int:
   global forms
   forms.put(form)


def dequeue () -> dict[str,str]:
   global forms
   return forms.get()