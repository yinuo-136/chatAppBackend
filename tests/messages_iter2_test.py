import pytest
import requests
from wrapper.channels_wrappers import clear, user_sign_up, user_create_channel
from wrapper.message_wrappers import send_message, senddm_message, edit_message, show_messages, show_dm_messages, remove_messages
from wrapper.dm_wrappers import dm_create_wrapper
from wrapper.auth_wrappers import auth_register
from src.config import url

BASE_URL = url
   
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

    payload = requests.get(f'{BASE_URL}/channel/messages/v2', params={'token': str(token),
                                                                'channel_id': channel_id,
                                                                'start': -20})
    
    assert payload.status_code == 400

#feature 6: end will return -1 if the message that need to be displayed is less than 50
def test_messages_end_return():

    clear()

    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    channel_id = user_create_channel(token, '12345', True)
    counter = 20
    while (counter > 0):
        send_message(token, channel_id, 'hello')
        counter -= 1

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
    counter = 100
    while (counter > 0):
        send_message(token, channel_id, 'hello')
        counter -= 1

    payload = requests.get(f'{BASE_URL}/channel/messages/v2', params={'token': token,
                                                                'channel_id': channel_id,
                                                                'start': 0})
    p = payload.json()
    assert p['end'] == 50

#############################################################################################################
##message_senddm_v1 tests
#feature 1: raise access error when token is invalid
#TO DO

#feature 2:raise input error when length of message is less than 1 or over 1000 characters

def test_senddm_less_1():
    clear()
    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    data_2 = auth_register('test2@gmail.com', 'password2', 'first2', 'last2')

    data = data_2.json()
    u_id_2 = data['auth_user_id']

    r = dm_create_wrapper(token_1, [u_id_2])
    r = r.json()
    dm_id = r['dm_id']
    

    payload = requests.post(f'{BASE_URL}/message/senddm/v1', json={'token': token_1,
                                                                'dm_id': dm_id,
                                                                'message': ""})
    
    assert payload.status_code == 400

def test_senddm_over_1000():
    clear()
    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    data_2 = auth_register('test2@gmail.com', 'password2', 'first2', 'last2')

    data = data_2.json()
    u_id_2 = data['auth_user_id']
    
    r = dm_create_wrapper(token_1, [u_id_2])
    r = r.json()
    dm_id = r['dm_id']
    

    payload = requests.post(f'{BASE_URL}/message/senddm/v1', json={'token': token_1,
                                                                'dm_id': dm_id,
                                                                'message': "a"*1200})
    
    assert payload.status_code == 400

#feature 3: raise input error if dm_id does not refer to a valid DM
def test_senddm_id_validity():
    clear()

    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    #a random not exist channel id
    dm_id = 12

    payload = requests.post(f'{BASE_URL}/message/senddm/v1', json={'token': token,
                                                                'dm_id': dm_id,
                                                                'message': "hello, world"})

    assert payload.status_code == 400

#featrue 4: raise access error when the authorised user is not a member of the DM
def test_message_senddm_not_a_member():
    clear()
    token_1 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last2') 
    data_2 = auth_register('test2@gmail.com', 'password2', 'first2', 'last2')
    token_3 = user_sign_up('test3@gmail.com', 'password3', 'first3', 'last3') 

    data = data_2.json()
    u_id_2 = data['auth_user_id']

    r = dm_create_wrapper(token_1, [u_id_2])
    r= r.json()
    dm_id = r['dm_id']

    payload = requests.post(f'{BASE_URL}/message/senddm/v1', json={'token': token_3,
                                                                'dm_id': dm_id,
                                                                'message': "hello, world"})
    
    assert payload.status_code == 403

#feature 5: two message id should be unique
def test_message_senddm_id_unique():
    clear()
    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    data_2 = auth_register('test2@gmail.com', 'password2', 'first2', 'last2')

    data = data_2.json()
    u_id_2 = data['auth_user_id']
    
    r = dm_create_wrapper(token_1, [u_id_2])
    r = r.json()
    dm_id = r['dm_id']

    p1 = senddm_message(token_1, dm_id, 'a')

    p2 = senddm_message(token_1, dm_id, 'b')

    assert p1 != p2

################################################################################################################
##message_edit_v1

#feature 1: raise input error when length of message is over 1000 characters
def test_message_edit_over_1000():
    clear()
    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    channel_id = user_create_channel(token, '12345', True)

    m_id = send_message(token, channel_id, 'hello')

    payload = edit_message(token, m_id, 'a'*1200)

    assert payload.status_code == 400

#feature 2: raise input error when message id does not exist
def test_message_edit_id_invalid():
    clear()
    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    m_id = 12

    payload = edit_message(token, m_id, 'a')

    assert payload.status_code == 400

#feature 3: raise input error when m_id is not valid in channel/DM that the user has joined
def test_messsage_edit_channel_not_join():
    clear()
    token_1 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')
    token_2 = user_sign_up('test2@gmail.com', 'password2', 'first2', 'last2')

    channel_id = user_create_channel(token_1, '12345', True)

    m_id = send_message(token_1, channel_id, 'hello')  

    payload = edit_message(token_2, m_id, 'a')

    assert payload.status_code == 400

def test_message_edit_dm_not_join():
    clear()
    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    data_2 = auth_register('test2@gmail.com', 'password2', 'first2', 'last2')
    token_3 = user_sign_up('test3@gmail.com', 'password3', 'first3', 'last3')

    data = data_2.json()
    u_id_2 = data['auth_user_id']
    
    r = dm_create_wrapper(token_1, [u_id_2])
    r = r.json()
    dm_id = r['dm_id']

    m_id = senddm_message(token_1, dm_id, 'hello')

    payload = edit_message(token_3, m_id, 'b')

    assert payload.status_code == 400

#feature 4: raise access error when the message wasn't sent by the authorised user making this 
# request and the authorised user does not have owner permissions in the channel/DM
'''
def test_message_edit_channel_no_permission():
   To Do
'''
def test_message_edit_dm_no_permission():
    clear()
    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    data_2 = auth_register('test2@gmail.com', 'password2', 'first2', 'last2')
    data_3 = auth_register('test3@gmail.com', 'password3', 'first3', 'last3')


    data_2 = data_2.json()
    data_3 = data_3.json()

    token_2 = data_2['token']
    token_3 = data_3['token']
    u_id_2 = data_2['auth_user_id']
    u_id_3 = data_3['auth_user_id']
    
    r = dm_create_wrapper(token_1, [u_id_2, u_id_3])
    r = r.json()
    dm_id = r['dm_id']

    m_id = senddm_message(token_2, dm_id, 'hello')

    payload = edit_message(token_3, m_id, 'b')

    assert payload.status_code == 403

#feature 5:  If the new message is an empty string, the message is deleted.
def test_message_edit__channel_empty_string():
    clear()
    token_1 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')

    channel_id = user_create_channel(token_1, '12345', True)

    m_id_1 = send_message(token_1, channel_id, 'hello1')  
    send_message(token_1, channel_id, 'hello2')

    edit_message(token_1, m_id_1, '')

    assert show_messages(token_1, channel_id, 0) == ['hello2']

def test_message_edit__dm_empty_string():
    clear()
    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    data_2 = auth_register('test2@gmail.com', 'password2', 'first2', 'last2')

    data = data_2.json()
    u_id_2 = data['auth_user_id']
    
    r = dm_create_wrapper(token_1, [u_id_2])
    r = r.json()
    dm_id = r['dm_id']

    m_id_1 = senddm_message(token_1, dm_id, 'hello')
    senddm_message(token_1, dm_id, 'hello2')
    payload = edit_message(token_1, m_id_1, '')

    assert payload.status_code == 200

    assert show_dm_messages(token_1, dm_id, 0) == ['hello2']

#feature 6: test the success case
def test_message_edit_success():
    clear()
    token_1 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')

    channel_id = user_create_channel(token_1, '12345', True)

    m_id_1 = send_message(token_1, channel_id, 'hello1')  
    send_message(token_1, channel_id, 'hello2')

    edit_message(token_1, m_id_1, 'hello3')

    assert show_messages(token_1, channel_id, 0) == ['hello2','hello3']

############################################################################################
##message_remove_v1 tests
#feature 1: raise input error when message id does not exist
def test_message_edit_id_invalid():
    clear()
    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    m_id = 12

    payload = remove_messages(token, m_id)

    assert payload.status_code == 400

#feature 2: raise input error when m_id is not valid in channel/DM that the user has joined
def test_messsage_remove_channel_not_join():
    clear()
    token_1 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')
    token_2 = user_sign_up('test2@gmail.com', 'password2', 'first2', 'last2')

    channel_id = user_create_channel(token_1, '12345', True)

    m_id = send_message(token_1, channel_id, 'hello')  

    payload = remove_messages(token_2, m_id)

    assert payload.status_code == 400

def test_message_remove_dm_not_join():
    clear()
    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    data_2 = auth_register('test2@gmail.com', 'password2', 'first2', 'last2')
    token_3 = user_sign_up('test3@gmail.com', 'password3', 'first3', 'last3')

    data = data_2.json()
    u_id_2 = data['auth_user_id']
    
    r = dm_create_wrapper(token_1, [u_id_2])
    r = r.json()
    dm_id = r['dm_id']

    m_id = senddm_message(token_1, dm_id, 'hello')

    payload = remove_messages(token_3, m_id)

    assert payload.status_code == 400

#feature 3: raise access error when the message wasn't sent by the authorised user making this 
# request and the authorised user does not have owner permissions in the channel/DM
'''
def test_message_remove_channel_no_permission():
   To Do
'''
def test_message_remove_dm_no_permission():
    clear()
    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    data_2 = auth_register('test2@gmail.com', 'password2', 'first2', 'last2')
    data_3 = auth_register('test3@gmail.com', 'password3', 'first3', 'last3')


    data_2 = data_2.json()
    data_3 = data_3.json()

    token_2 = data_2['token']
    token_3 = data_3['token']
    u_id_2 = data_2['auth_user_id']
    u_id_3 = data_3['auth_user_id']
    
    r = dm_create_wrapper(token_1, [u_id_2, u_id_3])
    r = r.json()
    dm_id = r['dm_id']

    m_id = senddm_message(token_2, dm_id, 'hello')

    payload = remove_messages(token_3, m_id)

    assert payload.status_code == 403

#feature 4: test the success case
def test_message_remove_success_channel():
    clear()
    token_1 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')

    channel_id = user_create_channel(token_1, '12345', True)

    m_id_1 = send_message(token_1, channel_id, 'hello1')  
    send_message(token_1, channel_id, 'hello2')

    remove_messages(token_1, m_id_1)

    assert show_messages(token_1, channel_id, 0) == ['hello2']

def test_message_remove_success_dm():
    clear()
    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    data_2 = auth_register('test2@gmail.com', 'password2', 'first2', 'last2')

    data = data_2.json()
    u_id_2 = data['auth_user_id']
    
    r = dm_create_wrapper(token_1, [u_id_2])
    r = r.json()
    dm_id = r['dm_id']

    m_id_1 = senddm_message(token_1, dm_id, 'hello1')
    senddm_message(token_1, dm_id, 'hello2')

    remove_messages(token_1, m_id_1)

    assert show_dm_messages(token_1, dm_id, 0) == ['hello2']
