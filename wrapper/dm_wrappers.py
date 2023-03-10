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


def dm_remove_wrapper(token, dm_id):

    payload = { 'token' : token,
                'dm_id' : dm_id } 

    headers = {'content-type': 'application/json'}

    return requests.delete(config.url + "dm/remove/v1", data=json.dumps(payload), headers=headers)


def dm_details_wrapper(token, dm_id):

    payload = { 'token' : token,
                'dm_id' : dm_id } 

    return requests.get(config.url + "dm/details/v1", params=payload)


def dm_leave_wrapper(token, dm_id):

    payload = {'token' : token, 
               'dm_id' : dm_id}

    
    return requests.post(config.url + "dm/leave/v1", json=payload)


def dm_messages_wrapper(token, dm_id, start):

    payload = { 'token' : token,
                'dm_id' : dm_id,
                'start' : start } 

    return requests.get(config.url + "dm/messages/v1", params=payload)