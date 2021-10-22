import pytest
import requests
import json
from src import config
from src.channel import channel_addowner_v1, channel_removeowner_v1
from wrapper.auth_wrappers import auth_register
from wrapper.channel_wrappers import channel_details
from wrapper.clear_wrapper import clear_http
from src.data_store import data_store

ACCESS_ERROR = 403
INPUT_ERROR = 400

#Waiting for channel_create to get wrapped up

#channel/addowner/v1 
#InputError if channel_id does not refer to a valid channel
def test_addowner_channel_id_valid():
    clear_http()

    r = auth_register("test@gmail.com", "password", "First", "Last")
    token = r.json()['token']

    r1 = channel_addowner_v1(token, 99, 1)
    
    assert r1.status_code == INPUT_ERROR


#InputError if u_id does not refer to a valid user
def test_addowner_user_id_valid():
    clear_http()

    r = auth_register("test@gmail.com", "password", "First", "Last")
    token = r.json()['token']

    r1 = channel_addowner_v1(token, 1, 99)

    assert r1.status_code == INPUT_ERROR

#InputError if u_id refers to a user who is not a member of channel

#InputError if u_id refers to a user who is already an owner of channel

#AccessError if channel_id is valid and auth user does not have owner perms

#Test function output

#channel/removeowner/v1
#InputError if channel_id does not refer to a valid channel

#InputError if u_id does not refer to a valid user

#InputError if u_id refers to a user who is not the owner of channel

#InputError if u_id refers to a user who is the only owner of channel

#AccessError if channel_id is valid but auth user does not have owner perms

#Test function output
