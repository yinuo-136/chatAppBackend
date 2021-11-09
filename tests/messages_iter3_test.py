import pytest
import requests
from wrapper.channels_wrappers import clear, user_sign_up, user_create_channel
from wrapper.message_wrappers import send_message, senddm_message, edit_message, share_messages, react_message, unreact_message, pin_message, unpin_message
from wrapper.dm_wrappers import dm_create_wrapper
from wrapper.auth_wrappers import auth_register
from wrapper.channel_wrappers import channel_join
from src.config import url
from time import sleep
from datetime import datetime, timezone
from wrapper.clear_wrapper import clear_http
from wrapper.message_wrappers import sendlater_ch, sendlater_dm, show_messages, show_dm_messages, send_message, senddm_message

INPUT_ERROR = 400
ACCESS_ERROR = 403
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
def test_share_message_successful_channel_one():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    channel_id_1 = user_create_channel(token_1, '12345', True)

    m_id = send_message(token_1, channel_id_1, 'hello')

    payload = share_messages(token_1, m_id, '@firstlast abc' , channel_id_1, -1)
    share_messages(token_1, m_id, '@firstlast abc' , channel_id_1, -1)

    assert payload.status_code == 200

def test_share_message_successful_channel_two():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    channel_id_1 = user_create_channel(token_1, '12345', True)

    m_id = send_message(token_1, channel_id_1, 'hello')

    payload = share_messages(token_1, m_id, 'abc' , channel_id_1, -1)

    assert payload.status_code == 200

def test_share_message_successful_dm_one():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    dm_info = dm_create_wrapper(token_1, [])
    dm_id_1 = dm_info.json()['dm_id']
    m_id = senddm_message(token_1, dm_id_1, 'hello')

    payload = share_messages(token_1, m_id, '@firstlast abc', -1, dm_id_1)
    share_messages(token_1, m_id, '@firstlast abc', -1, dm_id_1)

    assert payload.status_code == 200

def test_share_message_successful_dm_two():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    dm_info = dm_create_wrapper(token_1, [])
    dm_id_1 = dm_info.json()['dm_id']
    m_id = senddm_message(token_1, dm_id_1, 'hello')

    payload = share_messages(token_1, m_id, 'abc', -1, dm_id_1)

    assert payload.status_code == 200

####################################################################################################3
##message_react_v1 tests
#feature 1: raise InpuError when message_id does not exist
def test_message_react_m_id_not_exist():
    clear()

    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    m_id = 12
    react_id = 1

    payload = react_message(token, m_id, react_id)

    assert payload.status_code == 400

#feature 2: raise InputError when message_id is not a valid message within a channel or DM that the authorised user has joined
def test_message_react_not_within_channel():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    token_2 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')

    channel_id_1 = user_create_channel(token_1, '12345', True)
    m_id = send_message(token_1, channel_id_1, 'hello')

    react_id = 1

    payload = react_message(token_2, m_id, react_id)

    assert payload.status_code == 400

def test_message_react_not_winthin_dm():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    token_2 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')


    dm_info = dm_create_wrapper(token_1, [])
    dm_id_1 = dm_info.json()['dm_id']
    m_id = senddm_message(token_1, dm_id_1, 'hello')

    react_id = 1

    payload = react_message(token_2, m_id, react_id)

    assert payload.status_code == 400

#feature 3: raise InputError when react ID is not a valid id
def test_message_react_id_invalid():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    channel_id_1 = user_create_channel(token_1, '12345', True)
    m_id = send_message(token_1, channel_id_1, 'hello')
    react_id = 2

    payload = react_message(token_1, m_id, react_id)

    assert payload.status_code == 400

#feature 4: raise InputError when the message already contains a react with ID react_id from the authorised user
def test_message_react_already_reacted():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    channel_id_1 = user_create_channel(token_1, '12345', True)
    m_id = send_message(token_1, channel_id_1, 'hello')
    react_id = 1

    react_message(token_1, m_id, react_id)

    payload = react_message(token_1, m_id, react_id)

    assert payload.status_code == 400

#feature 5: test successful case
def test_successful_message_react_channel_one():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    channel_id_1 = user_create_channel(token_1, '12345', True)
    m_id = send_message(token_1, channel_id_1, 'hello')
    react_id = 1

    payload = react_message(token_1, m_id, react_id)

    assert payload.status_code == 200

def test_successful_message_react_dm():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    dm_info = dm_create_wrapper(token_1, [])
    dm_id_1 = dm_info.json()['dm_id']
    m_id = senddm_message(token_1, dm_id_1, 'hello')

    react_id = 1

    payload = react_message(token_1, m_id, react_id)

    assert payload.status_code == 200

def test_successful_message_react_channel_two():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    channel_id_1 = user_create_channel(token_1, '12345', True)
    m_id_1 = send_message(token_1, channel_id_1, 'hello')
    m_id_2 = send_message(token_1, channel_id_1, 'hello1')
    react_id = 1
    

    payload = react_message(token_1, m_id_1, react_id)
    react_message(token_1, m_id_2, react_id)

    assert payload.status_code == 200

#########################################################################################################
##message_unreact_v1 tests
#feature 1: raise InpuError when message_id does not exist
def test_message_unreact_m_id_not_exist():
    clear()

    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    m_id = 12
    react_id = 1

    payload = unreact_message(token, m_id, react_id)

    assert payload.status_code == 400

#feature 2: raise InputError when message_id is not a valid message within a channel or DM that the authorised user has joined
def test_message_unreact_not_within_channel():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    token_2 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')

    channel_id_1 = user_create_channel(token_1, '12345', True)
    m_id = send_message(token_1, channel_id_1, 'hello')

    react_id = 1

    payload = unreact_message(token_2, m_id, react_id)

    assert payload.status_code == 400

def test_message_unreact_not_winthin_dm():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    token_2 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')


    dm_info = dm_create_wrapper(token_1, [])
    dm_id_1 = dm_info.json()['dm_id']
    m_id = senddm_message(token_1, dm_id_1, 'hello')

    react_id = 1

    payload = unreact_message(token_2, m_id, react_id)

    assert payload.status_code == 400

#feature 3: raise InputError when react ID is not a valid id
def test_message_unreact_id_invalid():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    channel_id_1 = user_create_channel(token_1, '12345', True)
    m_id = send_message(token_1, channel_id_1, 'hello')
    react_id = 2

    payload = unreact_message(token_1, m_id, react_id)

    assert payload.status_code == 400

#feature 4: raise InputError when the message already contains a react with ID react_id from the authorised user
def test_message_unreact_does_not_reacted():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    channel_id_1 = user_create_channel(token_1, '12345', True)
    m_id = send_message(token_1, channel_id_1, 'hello')
    react_id = 1

    payload = unreact_message(token_1, m_id, react_id)

    assert payload.status_code == 400

#feature 5: test successful case
def test_successful_message_unreact_channel():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    channel_id_1 = user_create_channel(token_1, '12345', True)
    m_id = send_message(token_1, channel_id_1, 'hello')
    react_id = 1

    react_message(token_1, m_id, react_id)
    payload = unreact_message(token_1, m_id, react_id)

    assert payload.status_code == 200

def test_successful_message_unreact_dm():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')

    dm_info = dm_create_wrapper(token_1, [])
    dm_id_1 = dm_info.json()['dm_id']
    m_id = senddm_message(token_1, dm_id_1, 'hello')

    react_id = 1

    react_message(token_1, m_id, react_id)
    payload = unreact_message(token_1, m_id, react_id)

    assert payload.status_code == 200


###################################################################################################################
##message_pin_v1 tests
#feature 1: raise InputError if message_id does not exist
def test_message_pin_m_id_not_exist():
    clear()

    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    m_id = 12

    payload = pin_message(token, m_id)

    assert payload.status_code == 400

#feature 2: raise InputError when message_id is not a valid message within a channel or DM that the authorised user has joined
def test_message_pin_m_id_not_valid_channel():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    token_2 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')

    channel_id_1 = user_create_channel(token_1, '12345', True)
    m_id = send_message(token_1, channel_id_1, 'hello')

    payload = pin_message(token_2, m_id)

    assert payload.status_code == 400

def test_message_pin_m_id_not_vlaid_dm():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    token_2 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')


    dm_info = dm_create_wrapper(token_1, [])
    dm_id_1 = dm_info.json()['dm_id']
    m_id = senddm_message(token_1, dm_id_1, 'hello')

    payload = pin_message(token_2, m_id)

    assert payload.status_code == 400 

#feature 3: raise AccessError when  the authorised user does not have owner permissions in the channel/DM
def test_message_pin_no_permission_channel():
    clear()
    token_1 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')
    token_2 = user_sign_up('test2@gmail.com', 'password2', 'first2', 'last2')

    channel_id = user_create_channel(token_1, '12345', True)

    m_id = send_message(token_1, channel_id, 'hello')  

    channel_join(token_2, channel_id)
    
    payload = pin_message(token_2, m_id)

    assert payload.status_code == 403

def test_message_pin_no_permission_dm():
    clear()
    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    data_2 = auth_register('test2@gmail.com', 'password2', 'first2', 'last2')

    data_2 = data_2.json()

    token_2 = data_2['token']
    u_id_2 = data_2['auth_user_id']
    
    r = dm_create_wrapper(token_1, [u_id_2])
    r = r.json()
    dm_id = r['dm_id']

    m_id = senddm_message(token_2, dm_id, 'hello')

    payload = pin_message(token_2, m_id)

    assert payload.status_code == 403

#feature 4: raise InputError if the message is already pinned
def test_message_pin_already_pinned():
    clear()
    token_1 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')

    channel_id = user_create_channel(token_1, '12345', True)

    m_id = send_message(token_1, channel_id, 'hello')  
    
    pin_message(token_1, m_id)
    payload = pin_message(token_1, m_id)

    assert payload.status_code == 400

#feature 5: test successful case
def test_message_pin_successful_channel():
    clear()
    token_1 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')

    channel_id = user_create_channel(token_1, '12345', True)

    m_id = send_message(token_1, channel_id, 'hello')  
    
    payload = pin_message(token_1, m_id)

    assert payload.status_code == 200

def test_message_pin_successful_dm():
    clear()
    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    data_2 = auth_register('test2@gmail.com', 'password2', 'first2', 'last2')

    data_2 = data_2.json()

    token_2 = data_2['token']
    u_id_2 = data_2['auth_user_id']
    
    r = dm_create_wrapper(token_1, [u_id_2])
    r = r.json()
    dm_id = r['dm_id']

    m_id = senddm_message(token_2, dm_id, 'hello')

    payload = pin_message(token_1, m_id)

    assert payload.status_code == 200

########################################################################################################
##message_unpin_v1 tests
#feature 1: raise InputError if message_id does not exist
def test_message_unpin_m_id_not_exist():
    clear()

    token = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    m_id = 12

    payload = unpin_message(token, m_id)

    assert payload.status_code == 400

#feature 2: raise InputError when message_id is not a valid message within a channel or DM that the authorised user has joined
def test_message_unpin_m_id_not_valid_channel():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    token_2 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')

    channel_id_1 = user_create_channel(token_1, '12345', True)
    m_id = send_message(token_1, channel_id_1, 'hello')

    payload = unpin_message(token_2, m_id)

    assert payload.status_code == 400

def test_message_unpin_m_id_not_vlaid_dm():
    clear()

    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    token_2 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')


    dm_info = dm_create_wrapper(token_1, [])
    dm_id_1 = dm_info.json()['dm_id']
    m_id = senddm_message(token_1, dm_id_1, 'hello')

    payload = unpin_message(token_2, m_id)

    assert payload.status_code == 400 

#feature 3: raise AccessError when  the authorised user does not have owner permissions in the channel/DM
def test_message_unpin_no_permission_channel():
    clear()
    token_1 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')
    token_2 = user_sign_up('test2@gmail.com', 'password2', 'first2', 'last2')

    channel_id = user_create_channel(token_1, '12345', True)

    m_id = send_message(token_1, channel_id, 'hello')  

    channel_join(token_2, channel_id)
    
    payload = unpin_message(token_2, m_id)

    assert payload.status_code == 403

def test_message_unpin_no_permission_dm():
    clear()
    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    data_2 = auth_register('test2@gmail.com', 'password2', 'first2', 'last2')

    data_2 = data_2.json()

    token_2 = data_2['token']
    u_id_2 = data_2['auth_user_id']
    
    r = dm_create_wrapper(token_1, [u_id_2])
    r = r.json()
    dm_id = r['dm_id']

    m_id = senddm_message(token_2, dm_id, 'hello')

    payload = unpin_message(token_2, m_id)

    assert payload.status_code == 403

#feature 4: raise InputError if the message is not already pinned
def test_message_unpin_not_pinned():
    clear()
    token_1 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')

    channel_id = user_create_channel(token_1, '12345', True)

    m_id = send_message(token_1, channel_id, 'hello')  
    
    payload = unpin_message(token_1, m_id)

    assert payload.status_code == 400

#feature 5: test successful case
def test_message_unpin_successful_channel():
    clear()
    token_1 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')

    channel_id = user_create_channel(token_1, '12345', True)

    m_id = send_message(token_1, channel_id, 'hello')  
    
    pin_message(token_1, m_id)
    payload = unpin_message(token_1, m_id)

    assert payload.status_code == 200

def test_message_unpin_successful_dm():
    clear()
    token_1 = user_sign_up('test@gmail.com', 'password', 'first', 'last')
    data_2 = auth_register('test2@gmail.com', 'password2', 'first2', 'last2')

    data_2 = data_2.json()

    token_2 = data_2['token']
    u_id_2 = data_2['auth_user_id']
    
    r = dm_create_wrapper(token_1, [u_id_2])
    r = r.json()
    dm_id = r['dm_id']

    m_id = senddm_message(token_2, dm_id, 'hello')

    pin_message(token_1, m_id)
    payload = unpin_message(token_1, m_id)

    assert payload.status_code == 200

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

def test_sendlater_channel_basic_one(current_time):
    clear_http()
    
    r1 = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    token = r1.json()['token']
    user_create_channel(token, "channelname", True)
    
    r = sendlater_ch(token, 1, "@jaydenmatthews this is a message", current_time + 1)
    
    sleep(1)    #Wait for message to send
    
    assert r.json() == {'message_id' : 1}
    
    assert show_messages(token, 1, 0) == ['@jaydenmatthews this is a message']

    
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

def test_sendlater_dm_basic_one(current_time):
    clear_http()
    
    r = auth_register("jaymatt2232@gmail.com", "password", "jayden", "matthews")
    r1 = auth_register("nick@gmail.com", "password", "nick", "stath")
    
    u_id = r1.json()['auth_user_id']
    token = r.json()['token']
    
    dm_create_wrapper(token, [u_id])
    
    r2 = sendlater_dm(token, 1, "@jaydenmatthews this is a message", current_time + 1)
    
    sleep(1)    #Wait for message to send
    
    assert r2.json() == {'message_id' : 1}
    
    assert show_dm_messages(token, 1, 0) == ['@jaydenmatthews this is a message']
    
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

