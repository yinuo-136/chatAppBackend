import pytest
import requests
from src.config import url

#######################################################################################
BASE_URL = url

def clear():
    requests.delete(f'{BASE_URL}/clear/v1')


def user_sign_up(email, password, first, last):
    payload = requests.post(f'{BASE_URL}/auth/register/v2', json= {'email': email,
                                                            'password': password,
                                                            'name_first': first,
                                                            'name_last': last})
    p = payload.json()
    return p['token']

def user_create_channel(token, name, is_public):
    payload = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token,
                                                            'name': name,
                                                            'is_public': is_public})
    p = payload.json()
    return p['channel_id']

def send_message(token, channel_id, message):
    requests.post(f'{BASE_URL}/message/send/v1', json={'token': token,
                                                                'channel_id': channel_id,
                                                                'message': message})
    
#########################################################################################
##message_send_v1 test
#feature 1: raise input error when channel_id does not refer to a valid channel
def test_message_send_channel_valid():
    clear()

    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    #a random not exist channel id
    channel_id = 12

    payload = requests.post(f'{BASE_URL}/message/send/v1', json={'token': token,
                                                                'channel_id': channel_id,
                                                                'message': "hello, world"})

    assert payload.status_code == 400

#feature 2: raise access error when token is invalid
#TO DO

#feature 3: raise input error when message is less than 1 or over 1000 characters 
def test_message_send_less_1():
    clear()
    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    channel_id = user_create_channel(token, '12345', True)

    payload = requests.post(f'{BASE_URL}/message/send/v1', json={'token': token,
                                                                'channel_id': channel_id,
                                                                'message': ""})
    
    assert payload.status_code == 400

def test_message_send_over_1000():
    clear()
    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    channel_id = user_create_channel(token, '12345', True)

    payload = requests.post(f'{BASE_URL}/message/send/v1', json={'token': token,
                                                                'channel_id': channel_id,
                                                                'message': "a"*1200})
    
    assert payload.status_code == 400

#featrue 4: raise access error when the authorised user is not a member of the channel
def test_message_send_not_a_member():
    clear()
    token_1 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last2') 
    token_2 = user_sign_up('test2@gmail.com', 'password2', 'first2', 'last2') 
    channel_id = user_create_channel(token_1, '12345', True)

    payload = requests.post(f'{BASE_URL}/message/send/v1', json={'token': token_2,
                                                                'channel_id': channel_id,
                                                                'message': "hello, world"})
    
    assert payload.status_code == 403

#featrue 5: two message id should be unique
def test_message_send_id_unique():
    clear()
    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    channel_id = user_create_channel(token, '12345', True)

    payload_1 = requests.post(f'{BASE_URL}/message/send/v1', json={'token': token,
                                                                'channel_id': channel_id,
                                                                'message': "a"})

    payload_2 = requests.post(f'{BASE_URL}/message/send/v1', json={'token': token,
                                                                'channel_id': channel_id,
                                                                'message': "b"})

    p1 = payload_1.json()
    p1 = p1['message_id']
    p2 = payload_2.json()
    p2 = p2['message_id']
    assert p1 != p2

########################################################################################
##channel_messages_v2
#feature 1: raise Accesserror if token does not refer to a valid user(or session_id)
'''
def test_user_id_validity_messages():
'''
    
#feature 2: raise Accesserror if user is not a member in the channel
def test_user_ismember_messages():

    clear()
    token_1 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1') 
    token_2 = user_sign_up('test2@gmail.com', 'password2', 'first2', 'last2') 
    channel_id = user_create_channel(token_1, '12345', True)

    payload = requests.get(f'{BASE_URL}/channel/messages/v2', params={'token': token_2,
                                                                'channel_id': channel_id,
                                                                'start': 0})
    assert payload.status_code == 403


#feature 3: raise Inputerror if channel_id is invalid
def test_channel_isvalid_messages():
    clear()

    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    #a random not exist channel id
    channel_id = 12

    payload = requests.get(f'{BASE_URL}/channel/messages/v2', params={'token': token,
                                                                'channel_id': channel_id,
                                                                'start': 0})

    assert payload.status_code == 400

#feature 4: raise InputError if start is greater than the total number 
# of messages in the channel
def test_start_isgreat_message():
    clear()

    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    channel_id = user_create_channel(token, '12345', True)

    payload = requests.get(f'{BASE_URL}/channel/messages/v2', params={'token': token,
                                                                'channel_id': channel_id,
                                                                'start': 20})
    
    assert payload.status_code == 400

#feature 5: raise InputError if start is less than zero
def test_start_less_than_zero():
    clear()

    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    channel_id = user_create_channel(token, '12345', True)

    payload = requests.get(f'{BASE_URL}/channel/messages/v2', params={'token': token,
                                                                'channel_id': channel_id,
                                                                'start': -20})
    
    assert payload.status_code == 400

#feature 6: end will return -1 if the message that need to be displayed is less than 50
def test_messages_end_return():

    clear()

    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    channel_id = user_create_channel(token, '12345', True)
    for i in range(20):
        send_message(token, channel_id, 'hello')

    payload = requests.get(f'{BASE_URL}/channel/messages/v2', params={'token': token,
                                                                'channel_id': channel_id,
                                                                'start': 0})
    p = payload.json()
    assert p['end'] == -1
    
#feature 7: end will return start + 50 if the message that need to be displayed is more than or equal to 50
def test_messages_end_return_1():

    clear()

    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    channel_id = user_create_channel(token, '12345', True)
    for i in range(100):
        send_message(token, channel_id, 'hello')

    payload = requests.get(f'{BASE_URL}/channel/messages/v2', params={'token': token,
                                                                'channel_id': channel_id,
                                                                'start': 0})
    p = payload.json()
    assert p['end'] == 50
