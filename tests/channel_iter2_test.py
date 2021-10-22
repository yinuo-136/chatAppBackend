import pytest
import requests
import json
from src import config
from wrapper.auth_wrappers import auth_register, auth_login, auth_logout
from wrapper.channel_wrappers import channel_details, channel_join, channel_invite
from wrapper.channels_wrappers import user_create_channel 
from wrapper.clear_wrapper import clear_http



@pytest.fixture
def channel_setup_register_user():
    clear_http()
    #r = auth_register("test1@gmail.com", "password123", "John", "Smith")
    

@pytest.fixture
def create_channel_public():
    clear_http()
    #r = user_create_channel("token", "PublicChannel1", TRUE)
    
@pytest.fixture
def create_channel_private():
    clear_http()
    #user_create_channel("token", "PublicChannel1", FALSE)
	


def test_basic_channel_details():
    clear_http()
    
    
def test_channel_inv_channelid_invaild():
    clear_http()
    r = auth_register("test1@gmail.com", "password123", "John", "Smith")
    data = r.json()
    user_token = data['token']
    u_id = data['auth_user_id']
    invalid_channel = 999
    r1 = channel_invite(user_token, invalid_channel, u_id)
    assert r1.status_code == 400

def test_channel_join_channelid_invaild():
    clear_http()
    r = auth_register("test1@gmail.com", "password123", "John", "Smith")
    data = r.json()
    user_token = data['token']
    invalid_channel = 999
    r1 = channel_join(user_token, invalid_channel)
    assert r1.status_code == 400
   
def test_channel_inv_user_id_invalid():
    clear_http()
    r = auth_register("test1@gmail.com", "password123", "John", "Smith")
    data = r.json()
    user_token = data['token']
    invalid_uid = 999
    channel = data['channel_id']
    r1 = channel_invite(user_token, channel, invalid_uid)
    assert r1.status_code == 400

def test_channel_inv_uid_already_member():
    clear_http()
    r = auth_register("test1@gmail.com", "password123", "John", "Smith")
    data = r.json()
    user_token = data['token']
    channel = data['channel_id']
    u_id = data['auth_user_id']
    c_id = user_create_channel(user_token, channel, FALSE)
    r1 = channel_invite(
    assert r1.status_code == 400
    #user_create_channel("token", "PublicChannel1", FALSE)
    

    
    
    
