import json
import os
from src.data_store import data_store


def save_datastore():
    with open('src/database.json', "w") as FILE:
        json.dump(data_store.get(), FILE, indent = 4)

def load_datastore():
    if os.path.isfile('src/database.json') == False:
        # If the file is not there, the server has not been started
        pass
    else:
        with open('src/database.json', "r") as FILE:
            data_store.set(json.load(FILE))
            
