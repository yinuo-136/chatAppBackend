import pytest
import requests
from src.config import url

BASE_URL = url

def search_messages(token, query_str):
    payload = requests.get(f'{BASE_URL}/search/v1', params={'token': token,
                                                            'query_str': query_str})
    return payload