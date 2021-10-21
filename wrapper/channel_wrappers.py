#import pytest
import json
import requests
import jwt
from src import config

def channel_details(user_id, channel_id):
    pretoken = {
        'user_id' : user_id,
        'session_id' : 'assume_this_is_correct'
    }

    token = jwt.encode(pretoken, config.SECRET, algorithm = 'HS256')
    payload = {'token' : token, 'channel_id' : channel_id}

    return requests.get(config.url + "channel/details/v2", params = payload)
