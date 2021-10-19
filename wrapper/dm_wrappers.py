import pytest
import requests
import jwt
import json
from src import config


def dm_create_wrapper(token, u_ids):

    payload = {'token' : token, 
        'u_ids' : u_ids}

    
    return requests.post(config.url + "dm/create/v1", json=payload)