#import pytest
import json
import requests
import jwt
from src import config

def channel_details(token, channel_id):
    payload = {'token' : token, 'channel_id' : channel_id}

    return requests.get(config.url + "channel/details/v2", params = payload)
