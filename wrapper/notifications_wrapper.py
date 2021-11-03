import pytest
import requests
from src.config import url

BASE_URL = url

def get_notifications(token):
    payload = requests.get(f'{BASE_URL}/notifications/get/v1', params={'token': token})

    return payload