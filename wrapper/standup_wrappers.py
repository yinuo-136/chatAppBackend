import requests
from src import config


def standup_create_wrapper(token, channel_id, length):

    payload = {'token' : token, 
        'channel_id' : channel_id,
        'length' : length}

    
    return requests.post(config.url + "standup/start/v1", json=payload)