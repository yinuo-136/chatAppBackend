import requests
import json
from src import config
from wrapper.clear_wrapper import clear_http

BASE_URL = config.url

def test_clear__correct_return():

    r = clear_http()

    status_code = r.status_code
    response_data = json.loads(r.text)

    assert status_code == 200
    assert response_data == {}