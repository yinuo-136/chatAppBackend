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
    
def channel_invite(token, channel_id, u_id):
    payload = { 'token' : token,
        'channel_id' : channel_id, 
	'u_id' : u_id}
	    
    return requests.post(config.url + "channel/invite/v2", json = payload)
	
def channel_join(token, channel_id):
    payload = { 'token' : token,
        'channel_id' : channel_id }
	    
    return requests.post(config.url + "channel/join/v2", json = payload)
	

