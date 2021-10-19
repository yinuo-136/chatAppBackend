import pytest
import requests
import jwt
import json
from src import config


def dm_create_wrapper(token, u_ids):

    payload = {'token' : token, 
        'u_ids' : u_ids}

    
    return requests.post(config.url + "dm/create/v1", json=payload)


def dm_list_wrapper(token):

    payload = { 'token' : token } 

    return requests.get(config.url + "dm/list/v1", params=payload)