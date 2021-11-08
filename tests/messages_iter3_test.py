import pytest
from time import sleep
from datetime import datetime, timezone
from wrapper.clear_wrapper import clear_http
from wrapper.message_wrappers import sendlater_ch, sendlater_dm, show_messages, show_dm_messages, send_message, senddm_message
from wrapper.auth_wrappers import auth_register 
from wrapper.channels_wrappers import user_create_channel
from wrapper.dm_wrappers import dm_create_wrapper

INPUT_ERROR = 400
ACCESS_ERROR = 403

# Fixture for return current timestamp
@pytest.fixture
def current_time():    
    dt = datetime.now(timezone.utc)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    return int(timestamp)   
    

def test_sendlater_channel_basic(current_time):
    clear_http()
    
    r1 = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    token = r1.json()['token']
    user_create_channel(token, "channelname", True)
    
    r = sendlater_ch(token, 1, "this is a message", current_time + 3)
    
    sleep(3)    #Wait for message to send
    
    assert r.json() == {'message_id' : 1}
    
    assert show_messages(token, 1, 0) == ['this is a message']

    
def test_sendlater_dm_basic(current_time):
    clear_http()
    
    r = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    r1 = auth_register("nick@gmail.com", "password", "nick", "stath")
    
    u_id = r1.json()['auth_user_id']
    token = r.json()['token']
    
    dm_create_wrapper(token, [u_id])
    
    r2 = sendlater_dm(token, 1, "this is a message", current_time + 3)
    
    sleep(3)    #Wait for message to send
    
    assert r2.json() == {'message_id' : 1}
    
    assert show_dm_messages(token, 1, 0) == ['this is a message']
    
def test_sendlater_channel_multimessage(current_time):
    clear_http()
    
    r1 = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    token = r1.json()['token']
    user_create_channel(token, "channelname", True)
    
    send_message(token, 1, "other message")
    
    r = sendlater_ch(token, 1, "this is a message", current_time + 3)
    
    sleep(3)    #Wait for message to send
    
    assert r.json() == {'message_id' : 2}
    
    assert show_messages(token, 1, 0) == ['this is a message', 'other message']

    
def test_sendlater_dm_multimessage(current_time):
    clear_http()
    
    r = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    r1 = auth_register("nick@gmail.com", "password", "nick", "stath")
    
    u_id = r1.json()['auth_user_id']
    token = r.json()['token']
    
    dm_create_wrapper(token, [u_id])
    
    senddm_message(token, 1, "other message")
    
    r2 = sendlater_dm(token, 1, "this is a message", current_time + 3)
    
    sleep(3)    #Wait for message to send
    
    assert r2.json() == {'message_id' : 2}
    
    assert show_dm_messages(token, 1, 0) == ['this is a message', 'other message']
    
    
def test_sendlater_channel_invalid_id(current_time):
    clear_http()
    
    r1 = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    token = r1.json()['token']
    user_create_channel(token, "channelname", True)
    
    r = sendlater_ch(token, 999, "this is a message", current_time + 3)
    
    assert r.status_code == INPUT_ERROR
    
def test_sendlater_dm_invalid_id(current_time):
    clear_http()

    r = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    r1 = auth_register("nick@gmail.com", "password", "nick", "stath")
    
    u_id = r1.json()['auth_user_id']
    token = r.json()['token']
    
    dm_create_wrapper(token, [u_id])
    
    r2 = sendlater_dm(token, 999, "this is a message", current_time + 3)
    
    assert r2.status_code == INPUT_ERROR

def test_sendlater_channel_toolong(current_time):
    clear_http()

    r1 = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    token = r1.json()['token']
    user_create_channel(token, "channelname", True)
    
    r = sendlater_ch(token, 1, "a" * 1001, current_time + 3)
    
    assert r.status_code == INPUT_ERROR
    
def test_sendlater_dm_toolong(current_time):
    clear_http()
    
    r = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    r1 = auth_register("nick@gmail.com", "password", "nick", "stath")
    
    u_id = r1.json()['auth_user_id']
    token = r.json()['token']
    
    dm_create_wrapper(token, [u_id])
    
    r2 = sendlater_dm(token, 1, "a" * 1001, current_time + 3)
    
    assert r2.status_code == INPUT_ERROR

def test_sendlater_channel_invalid_time(current_time):
    clear_http()
    
    r1 = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    token = r1.json()['token']
    user_create_channel(token, "channelname", True)
    
    r = sendlater_ch(token, 1, "message", current_time - 10)
    
    assert r.status_code == INPUT_ERROR

def test_sendlater_dm_invalid_time(current_time):
    clear_http()
    
    r = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    r1 = auth_register("nick@gmail.com", "password", "nick", "stath")
    
    u_id = r1.json()['auth_user_id']
    token = r.json()['token']
    
    dm_create_wrapper(token, [u_id])
    
    r2 = sendlater_dm(token, 1, "message", current_time - 10)
    
    assert r2.status_code == INPUT_ERROR

