import requests
import json
from src import config

BASE_URL = config.url

def test_clear__correct_return():

    r = requests.delete(BASE_URL + "clear/v1")

    status_code = r.status_code
    response_data = json.loads(r.text)

    assert status_code == 200
    assert response_data == {}