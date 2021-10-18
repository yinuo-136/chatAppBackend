import requests
from src import config

BASE_URL = config.url

# FOR USE IN OTHER CLASSES
def clear_http():

    requests.delete(BASE_URL + "clear/v1")