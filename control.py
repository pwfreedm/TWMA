from threading import Thread

from core import dequeue
from db import *
from forms import Consent
from view import start_flask_app



def app_loop():
    should_quit = False
    while not should_quit:
        form = dequeue()
        

if __name__ == '__main__':
    control = Thread(target=app_loop)
    control.start()
    start_flask_app(debug=True)
    control.join()
