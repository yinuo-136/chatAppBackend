from typing import Any
import requests
import json
import jwt
from requests.api import request
from src import config
from src.other import clear_v1

from wrapper.standup_wrappers import standup_create_wrapper
from wrapper.auth_wrappers import auth_register
from wrapper.channels_wrappers import user_create_channel
from wrapper.clear_wrapper import clear_http


ACCESS_ERROR = 403
INPUT_ERROR = 400
SUCCESS = 200

'''
Parameters:{ token, channel_id, length }
'''

def test_standup_start__success__basic():

    # Clear

    clear_http()

    # Register a user


    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']
    
    r2 = auth_register("test2@gmail.com", "password123", "Nick", "Zollos")
    token2 = r2.json()['token']

    # create a channel


    c_id1 = user_create_channel(token, "testchannel1", False)


    # start a standup

    standup_response = standup_create_wrapper(token, c_id1, 60) #create for 60 seconds

    # check it returns 200 OK and a time_finish

    status_code = standup_response.status_code
    response_body = json.loads(standup_response.text)


    assert status_code == SUCCESS
    assert len(response_body) == 1 #it contains one field `time_finish`
