import pytest
import requests
from wrapper.channels_wrappers import clear, user_sign_up, user_create_channel
from wrapper.message_wrappers import send_message, senddm_message, edit_message, share_messages, react_message, unreact_message, pin_message, unpin_message
from wrapper.dm_wrappers import dm_create_wrapper
from wrapper.auth_wrappers import auth_register
from wrapper.channel_wrappers import channel_join
from wrapper.search_wrappers import search_messages
from src.config import url

####################################################################################################
##seach_v1 tests
#feature 1: raise InputError when length of query_str is less than 1 or over 1000 characters
def test_search_str_length_less_one():
    clear()

    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    payload = search_messages(token, "")

    assert payload.status_code == 400

def test_search_str_length_lover_one_thousand():
    clear()

    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    payload = search_messages(token, "a" * 1200)

    assert payload.status_code == 400

#feature 2: test successful case of the function
def test_search_successful_case_one():
    clear()

    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    payload = search_messages(token, "hello")

    assert payload.status_code == 200

    p = payload.json()
    assert p == {'messages': []}

def test_search_successful_case_two():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    channel_id_1 = user_create_channel(token_1, '12345', True)
    m_id = send_message(token_1, channel_id_1, 'hello')

    payload = search_messages(token_1, 'llo')

    assert payload.status_code == 200

    p = payload.json()
    p_info = p['messages'][0]
    assert p_info['message_id'] == m_id
    assert p_info['message'] == "hello"

def test_search_successful_case_three():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    channel_id_1 = user_create_channel(token_1, '12345', True)
    m_id = send_message(token_1, channel_id_1, 'hello')

    react_message(token_1, m_id, 1)

    payload = search_messages(token_1, 'llo')

    assert payload.status_code == 200

    p = payload.json()
    p_info = p['messages'][0]
    assert p_info['message_id'] == m_id
    assert p_info['message'] == "hello"

def test_search_successful_case_four():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    channel_id_1 = user_create_channel(token_1, '12345', True)
    m_id_1 = send_message(token_1, channel_id_1, 'hello')
    m_id_2 = send_message(token_1, channel_id_1, 'hello2')
    

    payload = search_messages(token_1, 'llo')

    assert payload.status_code == 200

    p = payload.json()
    p_info_1 = p['messages'][0]
    assert p_info_1['message_id'] == m_id_1
    assert p_info_1['message'] == "hello"

    p_info_2 = p['messages'][1]
    assert p_info_2['message_id'] == m_id_2
    assert p_info_2['message'] == "hello2"

def test_search_successful_case_five():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    channel_id_1 = user_create_channel(token_1, '12345', True)
    m_id_1 = send_message(token_1, channel_id_1, 'hello')
    m_id_2 = send_message(token_1, channel_id_1, 'no')
    

    payload = search_messages(token_1, 'llo')

    assert payload.status_code == 200

    p = payload.json()
    p_info_1 = p['messages'][0]
    assert p_info_1['message_id'] == m_id_1
    assert p_info_1['message'] == "hello"

    