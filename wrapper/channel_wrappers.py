import pytest
import requests
import json
from src import config

def channel_details(token, channel_id):
    payload = {'token' : token, 'channel_id' : channel_id}

    return requests.get(config.url + "channel/details/v2", params = payload)


def channel_addowner(token, channel_id, u_id):
    payload = {'token' : token, 'channel_id' : channel_id, 'u_id' : u_id}

    return requests.post(config.url + "channel/addowner/v1", json = payload)

def channel_removeowner(token, channel_id, u_id):
    payload = {'token' : token, 'channel_id' : channel_id, 'u_id' : u_id}

    return requests.post(config.url + "channel/removeowner/v1", json = payload)
    
def channel_invite(token, channel_id, u_id):
    payload = { 'token' : token, 'channel_id' : channel_id, 'u_id' : u_id}
	    
    return requests.post(config.url + "channel/invite/v2", json = payload)
	
def channel_join(token, channel_id):
    payload = { 'token' : token, 'channel_id' : channel_id }
	    
    return requests.post(config.url + "channel/join/v2", json = payload)

def channel_leave(token, channel_id):
    payload = { 'token' : token, 'channel_id' : channel_id }

    return requests.post(config.url + "channel/leave/v1", json = payload)
