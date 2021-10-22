import pytest
import requests
import json
from src import config
from src import channel
from src.channels import channels_create_v1
from src.server import channel_addowner
from wrapper.auth_wrappers import auth_register
from wrapper.channel_wrappers import channel_addowner, channel_removeowner
from wrapper.clear_wrapper import clear_http
from src.data_store import data_store

ACCESS_ERROR = 403
INPUT_ERROR = 400

#channel/addowner/v1 
#InputError if channel_id does not refer to a valid channel
def test_addowner_channel_id_valid():
    clear_http()

    r = auth_register("test@gmail.com", "password", "First", "Last")
    token = r.json()['token']

    r1 = channel_addowner(token, 99, 1)
    
    assert r1.status_code == INPUT_ERROR


#InputError if u_id does not refer to a valid user
def test_addowner_user_id_valid():
    clear_http()

    r = auth_register("test@gmail.com", "password", "First", "Last")
    token = r.json()['token']

    r1 = channel_addowner(token, 1, 99)

    assert r1.status_code == INPUT_ERROR


#InputError if u_id refers to a user who is not a member of channel
def test_addowner_channel_membership():
    clear_http()

    r = auth_register("test@gmail.com", "password", "First", "Last")
    token = r.json()['token']

    r1 = channel_addowner(token, 1, 1)

    assert r1.status_code == INPUT_ERROR


# #InputError if u_id refers to a user who is already an owner of channel
# def test_addowner_already_owner():
#     clear_http()

#     r = auth_register("test@gmail.com", "password", "First", "Last")
#     token = r.json()['token']
#     u_id = r['auth_user_id']
#     channel = channels_create_v1(token, "Name", False)
#     channel_id = channel['channel_id']

#     r1 = channel_addowner(token, channel_id, u_id)

#     assert r1.status_code == INPUT_ERROR


# #AccessError if channel_id is valid and auth user does not have owner perms
# def test_addowner_no_owner_permission():
#     clear_http()

#     r = auth_register("test@gmail.com", "password", "First", "Last")
#     token = r.json()['token']
#     user2 = auth_register("test2@gmail.com", "password", "First", "Last")
#     u2_id = user2['user_id']
#     channel = channels_create_v1(token, "Name", False)
#     channel_id = channel['channel_id']

#     r1 = channel_addowner(token, channel_id, u2_id)

#     assert r1.status_code == ACCESS_ERROR


#channel/removeowner/v1
#InputError if channel_id does not refer to a valid channel
def test_removeowner_channel_id_valid():
    clear_http()

    r = auth_register("test@gmail.com", "password", "First", "Last")
    token = r.json()['token']

    r1 = channel_removeowner(token, 99, 1)
    
    assert r1.status_code == INPUT_ERROR


#InputError if u_id does not refer to a valid user
def test_removeowner_user_id_valid():
    clear_http()

    r = auth_register("test@gmail.com", "password", "First", "Last")
    token = r.json()['token']

    r1 = channel_removeowner(token, 1, 99)

    assert r1.status_code == INPUT_ERROR


#InputError if u_id refers to a user who is not the owner of channel
def test_removeowner_channel_membership():
    clear_http()

    r = auth_register("test@gmail.com", "password", "First", "Last")
    token = r.json()['token']

    r1 = channel_removeowner(token, 1, 1)

    assert r1.status_code == INPUT_ERROR


# #InputError if u_id refers to a user who is the only owner of channel
# def test_removeowner_only_owner():
#     clear_http()

#     r = auth_register("test@gmail.com", "password", "First", "Last")
#     token = r.json()['token']
#     u_id = r['user_id']
#     channel = channels_create_v1(token, "Name", False)
#     channel_id = channel['channel_id']

#     r1 = channel_removeowner(token, channel_id, u_id)

#     assert r1.status_code == INPUT_ERROR

# #AccessError if channel_id is valid but auth user does not have owner perms
# def test_removeowner_no_owner_permission():
#     clear_http()

#     r = auth_register("test@gmail.com", "password", "First", "Last")
#     token = r.json()['token']
#     user2 = auth_register("test2@gmail.com", "password", "First", "Last")
#     u2_id = user2['user_id']
#     channel = channels_create_v1(token, "Name", False)
#     channel_id = channel['channel_id']

#     r1 = channel_removeowner(token, channel_id, u2_id)

#     assert r1.status_code == ACCESS_ERROR
