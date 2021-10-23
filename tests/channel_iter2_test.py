import pytest
import requests

from src.server import channel_addowner
from wrapper.auth_wrappers import auth_register, auth_login, auth_logout
from wrapper.channel_wrappers import channel_addowner, channel_removeowner, channel_details, channel_join, channel_invite
from wrapper.channels_wrappers import user_create_channel, channels_list, user_sign_up
from wrapper.user_wrappers import user_profile
from wrapper.clear_wrapper import clear_http

ACCESS_ERROR = 403
INPUT_ERROR = 400


'''
Channel Details:
InputError when:
      
        channel_id does not refer to a valid channel
      
      AccessError when:
      
        channel_id is valid and the authorised user is not a member of the channel

Channel Remove Owner:
    InputError when any of:
      
        channel_id does not refer to a valid channel
        u_id does not refer to a valid user
        u_id refers to a user who is not an owner of the channel
        u_id refers to a user who is currently the only owner of the channel
      
      AccessError when:
      
        channel_id is valid and the authorised user does not have owner permissions in the channel

Channel Add Owner:        
    InputError when any of:
      
        channel_id does not refer to a valid channel
        u_id does not refer to a valid user
        u_id refers to a user who is not a member of the channel
        u_id refers to a user who is already an owner of the channel
      
      AccessError when:
      
        channel_id is valid and the authorised user does not have owner permissions in the channel
'''


def test_basic_channel_details():
    clear_http()
    r1 = auth_register("test1@gmail.com", "password123", "Namey", "Name")
    token1 = r1.json()['token']
    u_id = r1.json()['auth_user_id']
    
    c_id = user_create_channel(token1, "channel1" , True)
    
    r2 = channel_details(token1, c_id)
    
    assert r2.json() == { 
                    'name' : "channel1",
                    'is_public' : True,
                    'owner_members' : [user_profile(token1, u_id).json().get('user')],
                    'all_members' : [user_profile(token1, u_id).json().get('user')]
    }


def test_basic_add_owner():
    clear_http()
    r1 = auth_register("test1@gmail.com", "password123", "Namey", "Name")
    token1 = r1.json()['token']
    
    c_id = user_create_channel(token1, "channel1" , True)
    
    r2 = auth_register("test2@gmail.com", "password123", "New", "Person")
    token2 = r2.json()['token']
    u_id2 = r2.json()['auth_user_id']    
    
    channel_join(token2, c_id)

    r3 = channel_addowner(token1, c_id, u_id2)
    assert r3.json() == {}
    assert r3.status_code == 200  

  
def test_basic_remove_owner():
    clear_http()
    r1 = auth_register("test1@gmail.com", "password123", "Namey", "Name")
    token1 = r1.json()['token']
    u_id = r1.json()['auth_user_id']
    
    c_id = user_create_channel(token1, "channel1" , True)
    
    r2 = auth_register("test2@gmail.com", "password123", "New", "Person")
    token2 = r2.json()['token']
    u_id2 = r2.json()['auth_user_id']  

    channel_join(token2, c_id)
    
    r3 = channel_addowner(token1, c_id, u_id2)
    assert r3.json() == {}
    
    r4 = channel_removeowner(token2, c_id, u_id)
    assert r4.json() == {} 
    assert r4.status_code == 200
   
      
def test_invalid_channel_id_details():
    clear_http()
    r1 = auth_register("test1@gmail.com", "password123", "Namey", "Name")
    token1 = r1.json()['token']
    
    user_create_channel(token1, "channel1" , True)
    
    r2 = channel_details(token1, 999)
    
    assert r2.status_code == INPUT_ERROR


def test_invalid_auth_user_details():
    clear_http()
    r1 = auth_register("test1@gmail.com", "password123", "Namey", "Name")
    token1 = r1.json()['token']
    
    c_id = user_create_channel(token1, "channel1" , True)

    token2 = user_sign_up("test2@gmail.com", "password1234", "Namey1", "Name1")
    
    r2 = channel_details(token2, c_id)
    
    assert r2.status_code == ACCESS_ERROR
  
    
def test_invalid_channel_id_remove():
    clear_http()
    r1 = auth_register("test1@gmail.com", "password123", "Namey", "Name")
    token1 = r1.json()['token']
    u_id = r1.json()['auth_user_id']
    
    user_create_channel(token1, "channel1" , True)
        
    r4 = channel_removeowner(token1, 999, u_id)
    assert r4.status_code == INPUT_ERROR    

def test_invalid_uid_remove():
    clear_http()
    r1 = auth_register("test1@gmail.com", "password123", "Namey", "Name")
    token1 = r1.json()['token']
    
    c_id = user_create_channel(token1, "channel1" , True)
       
    r4 = channel_removeowner(token1, c_id, 123)
    assert r4.status_code == INPUT_ERROR
    
def test_uid_notowner_remove():
    clear_http()
    r1 = auth_register("test1@gmail.com", "password123", "Namey", "Name")
    token1 = r1.json()['token']
    
    c_id = user_create_channel(token1, "channel1" , True)
    
    r2 = auth_register("test2@gmail.com", "password123", "New", "Person")
    u_id2 = r2.json()['auth_user_id']    
    
    r4 = channel_removeowner(token1, c_id, u_id2)
    assert r4.status_code == INPUT_ERROR
    
def test_uid_onlyowner_remove():
    clear_http()
    r1 = auth_register("test1@gmail.com", "password123", "Namey", "Name")
    token1 = r1.json()['token']
    u_id = r1.json()['auth_user_id']
    
    c_id = user_create_channel(token1, "channel1" , True)
    
    r4 = channel_removeowner(token1, c_id, u_id)
    assert r4.status_code == INPUT_ERROR
  
def test_auth_user_not_owner_remove():
    clear_http()
    r1 = auth_register("test1@gmail.com", "password123", "Namey", "Name")
    token1 = r1.json()['token']
    u_id = r1.json()['auth_user_id']
    
    c_id = user_create_channel(token1, "channel1" , True)
    
    r2 = auth_register("test2@gmail.com", "password123", "New", "Person")
    token2 = r2.json()['token']
    channel_join(token2, c_id) 
     
    r4 = channel_removeowner(token2, c_id, u_id)
    assert r4.status_code == ACCESS_ERROR


def test_invalid_channel_id_add():
    clear_http()

    r1 = auth_register("test1@gmail.com", "password123", "Namey", "Name")
    token1 = r1.json()['token']
    
    user_create_channel(token1, "channel1" , True)
    
    r2 = auth_register("test2@gmail.com", "password123", "New", "Person")
    u_id2 = r2.json()['auth_user_id'] 
    
    r3 = channel_addowner(token1, 999, u_id2)
    assert r3.status_code == INPUT_ERROR
    
def test_invalid_uid_add():
    clear_http()

    r1 = auth_register("test1@gmail.com", "password123", "Namey", "Name")
    token1 = r1.json()['token']
    c_id = user_create_channel(token1, "channel1" , True)
    
    auth_register("test2@gmail.com", "password123", "New", "Person")
    
    r3 = channel_addowner(token1, c_id, 123)
    assert r3.status_code == INPUT_ERROR
    
def test_uid_notmember_add():
    clear_http()

    r1 = auth_register("test1@gmail.com", "password123", "Namey", "Name")
    token1 = r1.json()['token']
    
    c_id = user_create_channel(token1, "channel1" , True)
    
    r2 = auth_register("test2@gmail.com", "password123", "New", "Person")
    u_id2 = r2.json()['auth_user_id']    
    
    r3 = channel_addowner(token1, c_id, u_id2)
    assert r3.status_code == INPUT_ERROR
    
def test_uid_alreadyowner_add():
    clear_http()

    r1 = auth_register("test1@gmail.com", "password123", "Namey", "Name")
    token1 = r1.json()['token']
    u_id = r1.json()['auth_user_id']
    
    c_id = user_create_channel(token1, "channel1" , True)
    
    r3 = channel_addowner(token1, c_id, u_id)
    assert r3.status_code == INPUT_ERROR


def test_auth_user_no_owner_permission_add():
    clear_http()
    r1 = auth_register("test1@gmail.com", "password123", "Namey", "Name")
    token1 = r1.json()['token']
    
    c_id = user_create_channel(token1, "channel1" , True)
    
    r2 = auth_register("test2@gmail.com", "password123", "New", "Person")
    token2 = r2.json()['token']

    r3 = auth_register("test3@gmail.com", "password1235", "Namey3", "Name3")
    token3 = r3.json()['token']
    u_id3 = r3.json()['auth_user_id']
    channel_join(token2, c_id)
    channel_join(token3, c_id) 
     
    r4 = channel_addowner(token2, c_id, u_id3)
    assert r4.status_code == ACCESS_ERROR






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


