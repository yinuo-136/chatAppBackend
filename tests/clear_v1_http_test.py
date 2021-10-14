import pytest
import requests
import json
from src import config

BASE_URL = config.url

# FOR USE IN OTHER CLASSES
@pytest.fixture
def clear_http_fixture():

    requests.delete(BASE_URL + "clear/v1")


def test_clear__correct_return():

    r = requests.delete(BASE_URL + "clear/v1")

    status_code = r.status_code
    response_data = json.loads(r.text)

    assert status_code == 200
    assert response_data == {}