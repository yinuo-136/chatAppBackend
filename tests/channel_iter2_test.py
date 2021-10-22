import pytest
import requests
import json
from src import config
from wrapper.auth_wrappers import auth_register, auth_login, auth_logout
from wrapper.channel_wrappers import channel_details, channel_join, channel_invite
from wrapper.channels_wrappers import user_create_channel, channels_list
from wrapper.clear_wrapper import clear_http


ACCESS_ERROR = 403
INPUT_ERROR = 400

def test_basic_join():
    clear_http()
    
    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']
    
    c_id = user_create_channel(token, "channelname", True)
    
    r2 = auth_register("test2@gmail.com", "password123", "Johnny", "Sins")
    token1 = r2.json()['token']
    
    r3 = channel_join(token1, c_id)
    
    assert r3.json() == {}
    
def test_basic_invite():
    clear_http()
    
    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']
    
    c_id = user_create_channel(token, "channelname", False)
    
    r2 = auth_register("test2@gmail.com", "password123", "Johnny", "Sins")
    u_id = r2.json()['auth_user_id']
    
    r3 = channel_invite(token, c_id, u_id)
    
    assert r3.json() == {}

def test_invalid_channel_id_join():
    clear_http()
    
    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']
    
    user_create_channel(token, "channelname", True)
    
    r2 = auth_register("test2@gmail.com", "password123", "Johnny", "Sins")
    token1 = r2.json()['token']
    
    r3 = channel_join(token1, 999)
    
    assert r3.status_code == INPUT_ERROR
    
def test_user_alr_member_join():
    clear_http()
    
    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']
    
    c_id = user_create_channel(token, "channelname", True)
    
    r2 = auth_register("test2@gmail.com", "password123", "Johnny", "Sins")
    token1 = r2.json()['token']
    
    r3 = channel_join(token1, c_id)
    
    assert r3.json() == {}
    
    # Should fail as user already joined
    r4 = channel_join(token1, c_id)
    
    assert r4.status_code == INPUT_ERROR
    
def test_private_ch_not_global_join():
    clear_http()
    
    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']
    
    c_id = user_create_channel(token, "channelname", False)
    
    r2 = auth_register("test2@gmail.com", "password123", "Johnny", "Sins")
    token1 = r2.json()['token']
    
    # Should fail as user isnt a global owner, and channel is private)
    r3 = channel_join(token1, c_id)
    
    assert r3.status_code == ACCESS_ERROR

def test_private_ch_is_global_join():
    clear_http()
    
    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']
    
    r2 = auth_register("test2@gmail.com", "password123", "Johnny", "Sins")
    token1 = r2.json()['token']
    
    c_id = user_create_channel(token1, "channelname", False)
    
    # Should work as user is a global owner, and channel is private)
    r3 = channel_join(token, c_id)
    
    assert r3.json() == {}

def test_invalid_channel_id_invite():
    clear_http()
    
    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']
    
    user_create_channel(token, "channelname", False)
    
    r2 = auth_register("test2@gmail.com", "password123", "Johnny", "Sins")
    u_id = r2.json()['auth_user_id']
    
    #Should fail due to invalid channel id
    r3 = channel_invite(token, 999, u_id)
    
    assert r3.status_code == INPUT_ERROR
    
    
def test_invalid_uid_invite():
    clear_http()
        
    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']
    
    c_id = user_create_channel(token, "channelname", False)
    
    auth_register("test2@gmail.com", "password123", "Johnny", "Sins")

    #Should fail due to invalid user id
    r3 = channel_invite(token, c_id, 123)
    
    assert r3.status_code == INPUT_ERROR
    
def test_uid_alr_member_invite():
    clear_http()
    
    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']
    
    c_id = user_create_channel(token, "channelname", True)
    
    r2 = auth_register("test2@gmail.com", "password123", "Johnny", "Sins")
    u_id = r2.json()['auth_user_id']
    token1 = r2.json()['token']
    
    channel_join(token1, c_id)
    
    #Should fail as user has already joined 
    r3 = channel_invite(token, c_id, u_id)
    
    assert r3.status_code == INPUT_ERROR
    
def test_auth_user_not_member_join():
    clear_http()
    
    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']
    
    c_id = user_create_channel(token, "channelname", False)
    
    r2 = auth_register("test2@gmail.com", "password123", "Johnny", "Sins")
    token1 = r2.json()['token']
    
    r4 = auth_register("test3@gmail.com", "password123", "Nick", "Stath")
    u_id1 = r4.json()['auth_user_id']
    
    # Should fail as Johnny Sins is not a member of channel 
    r3 = channel_invite(token1, c_id, u_id1)
    
    assert r3.status_code == ACCESS_ERROR

def test_basic_channel_list():
    clear_http()
    
    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']
    
    c_id1 = user_create_channel(token, "channelname1", False)
    c_id2 = user_create_channel(token, "channelname2", True)
    c_id3 = user_create_channel(token, "channelname3", False)
    
    r2 = auth_register("test2@gmail.com", "password123", "Johnny", "Sins")
    token1 = r2.json()['token']
    
    user_create_channel(token1, "channelname4", False)
    
    #Should list channelname1, channelname2, channelname3
    r3 = channels_list(token)
    
    assert r3.json() == {'channels': [
                                {'channel_id': c_id1,
                                    'name': 'channelname1'
                                },
                                {'channel_id': c_id2,
                                    'name': 'channelname2'
                                },
                                {'channel_id': c_id3,
                                    'name': 'channelname3'
                                }
    ]}

