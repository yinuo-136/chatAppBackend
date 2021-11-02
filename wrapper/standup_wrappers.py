import requests
from src import config


def standup_create_wrapper(token, channel_id, length):

    payload = {'token' : token, 
        'channel_id' : channel_id,
        'length' : length}

    
    return requests.post(config.url + "standup/start/v1", json=payload)


def standup_is_active_wrapper(token, c_id):

    payload = { 'token' : token,
                'channel_id' : c_id } 

    return requests.get(config.url + "standup/active/v1", params=payload)


def standup_send_wrapper(token, channel_id, message):

    payload = {'token' : token, 
        'channel_id' : channel_id,
        'message' : message}

    
    return requests.post(config.url + "standup/send/v1", json=payload)