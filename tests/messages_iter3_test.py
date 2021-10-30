import pytest
import requests
from wrapper.channels_wrappers import clear, user_sign_up, user_create_channel
from wrapper.message_wrappers import send_message, senddm_message, edit_message, share_messages, show_messages, show_dm_messages, remove_messages
from wrapper.dm_wrappers import dm_create_wrapper
from wrapper.auth_wrappers import auth_register
from wrapper.channel_wrappers import channel_join
from src.config import url

BASE_URL = url

#############################################################################################################################
##message_share_v1 tests
#feature 1: raise inputerror when both channel_id and dm_id are invalid
def test_message_share_both_id_invalid():
    clear()
    
    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    #a random not exist channel id and dm id
    channel_id = 12
    dm_id = 12

    payload = share_messages(token, 1, 'hello', channel_id, dm_id)
    assert payload.status_code == 400

#feature 2: raise Inputerror when neither channel_id nor dm_id are -1
def test_message_share_no_negative_one():
    clear()

    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    channel_id = user_create_channel(token, '12345', True)
    dm_info = dm_create_wrapper(token, [])
    dm_id = dm_info.json()['dm_id']

    payload = share_messages(token, 1, 'hello', channel_id, dm_id)
    assert payload.status_code == 400

#feature 3: raise accesserror when the pair of channel_id and dm_id are valid (i.e. one is -1, the other is valid) 
# and the authorised user has not joined the channel or DM they are trying to share the message to
def test_message_share_user_not_join_channel():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    token_2 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')
    channel_id = user_create_channel(token_1, '12345', True)

    payload = share_messages(token_2, 1, '', channel_id, -1)
    assert payload.status_code == 403

def test_message_share_user_not_join_DM():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    token_2 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')
    #create a dm
    dm_info = dm_create_wrapper(token_1, [])
    dm_id = dm_info.json()['dm_id']

    payload = share_messages(token_2, 1, '', -1, dm_id)
    assert payload.status_code == 403

#feature 4: raise InputError if og_message_id does not exist
def test_message_share_message_id_not_exist():
    clear()

    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    channel_id = user_create_channel(token, '12345', True)
    m_id = 12

    payload = share_messages(token, m_id, '', channel_id, -1)

    assert payload.status_code == 400


#feature 5: raise InputError if og_message_id does not refer to a valid message within a channel/DM that the authorised user has joined
def test_message_share_user_not_within_channel():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    token_2 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')

    channel_id_1 = user_create_channel(token_1, '12345', True)
    channel_id_2 = user_create_channel(token_2, '123456', True)
    m_id = send_message(token_1, channel_id_1, 'hello')

    payload = share_messages(token_2, m_id, 'add', channel_id_2, -1)

    assert payload.status_code == 400

def test_message_share_user_not_within_dm():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    token_2 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')


    dm_info = dm_create_wrapper(token_1, [])
    dm_id_1 = dm_info.json()['dm_id']
    m_id = senddm_message(token_1, dm_id_1, 'hello')
    dm_info = dm_create_wrapper(token_2, []) 
    dm_id_2 = dm_info.json()['dm_id']

    payload = share_messages(token_2, m_id, 'add', -1, dm_id_2)

    assert payload.status_code == 400

#feature 6: raise InputError when length of message is more than 1000 characters
def test_message_share_length_more_than_1000():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    channel_id_1 = user_create_channel(token_1, '12345', True)

    m_id = send_message(token_1, channel_id_1, 'hello')

    payload = share_messages(token_1, m_id, 'a'* 1200 , channel_id_1, -1)

    assert payload.status_code == 400

#feature 7: test success case of the function
def test_share_message_successful_channel():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    channel_id_1 = user_create_channel(token_1, '12345', True)

    m_id = send_message(token_1, channel_id_1, 'hello')

    payload = share_messages(token_1, m_id, 'abc' , channel_id_1, -1)

    assert payload.status_code == 200

def test_share_message_successful_dm():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    dm_info = dm_create_wrapper(token_1, [])
    dm_id_1 = dm_info.json()['dm_id']
    m_id = senddm_message(token_1, dm_id_1, 'hello')

    payload = share_messages(token_1, m_id, 'abc', -1, dm_id_1)

    assert payload.status_code == 200


