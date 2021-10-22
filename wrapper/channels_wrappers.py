import pytest
import requests
from src.config import url

BASE_URL = url

def clear():
    requests.delete(f'{BASE_URL}/clear/v1')


def user_sign_up(email, password, first, last):
    payload = requests.post(f'{BASE_URL}/auth/register/v2', json= {'email': email,
                                                            'password': password,
                                                            'name_first': first,
                                                            'name_last': last})
    p = payload.json()
    return p['token']

def user_create_channel(token, name, is_public):
    payload = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token,
                                                            'name': name,
                                                            'is_public': is_public})
    p = payload.json()
    return p['channel_id']
