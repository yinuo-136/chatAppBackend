import pytest
import requests
from wrapper.channels_wrappers import clear, user_sign_up
from src.config import url

BASE_URL = url
#########################################################################################################
## channels/create/v2 tests:

# channels/create/v2 feature 1: length of name is less than 1 or more than 20 characters, 
# if it fails the rule, raise an InputError(error code 400).
def test_create_name_validity_1():

    clear()

    token = user_sign_up('test@gmail.com', 'password', 'First', 'Last')

    payload = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token,
                                                            'name': '',
                                                            'is_public': True})

    #check if the error raises if length of the name is less than 1
    assert payload.status_code == 400


def test_create_name_validity_2(): 
    
    clear()

    token = user_sign_up('test@gmail.com', 'password', 'First', 'Last')

    payload = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token,
                                                            'name': 'a'*50,
                                                            'is_public': True})

    #check if the error raises if length of the name is less than 20
    assert payload.status_code == 400


# channels_create_v1 feature 2: if the user didn't input the correct u_id or session_id（not exist), raise an 
# AccessError.
def test_create_s_id_validity():

    clear()

    # generate a token that doesn't exist.
    token = user_sign_up('test@gmail.com', 'password', 'First', 'Last')
    requests.post(f'{BASE_URL}/auth/logout/v1', json={'token': token})

    payload = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token,
                                                            'name': 'correct_name',
                                                            'is_public': True})
    assert payload.status_code == 403

def test_create_uid_validity():
    clear()
    #generate a token that the user_id is removed.
    token = user_sign_up('test@gmail.com', 'password', 'First', 'Last')
    #clear again to make the u_id invalid
    clear()

    payload = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token,
                                                            'name': 'correct_name',
                                                            'is_public': True})
    assert payload.status_code == 403

# channels_create_v1 feature 3: if both InputError(caused by name) and AccessError(caused by u_id or seesion_id)
#  should've raised, raised AccessError
def test_which_error_raised():
    
    clear()

    token = user_sign_up('test@gmail.com', 'password', 'First', 'Last')
    requests.post(f'{BASE_URL}/auth/logout/v1', json={'token': token})

    payload = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token,
                                                            'name': '',
                                                            'is_public': True})
    assert payload.status_code == 403
    


# channels_create_v1 feature 4:  eachtime the channel_id that created by the function should
#  be unique.
def test_create_id_unique():

    clear()

    token = user_sign_up('test@gmail.com', 'password', 'First', 'Last')

    payload_1 = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token,
                                                            'name': 'correct1',
                                                            'is_public': True})

    payload_2 = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token,
                                                            'name': 'correct2',
                                                            'is_public': True})
    p1 = payload_1.json()
    p2 = payload_2.json()
    assert p1['channel_id'] != p2['channel_id'] 

###################################################################################

## channels_listall_v1 tests

#feature 1: if there is no channels that has been created, return an empty list
def test_listall_empty_channel():

    clear()

    token = user_sign_up('test@gmail.com', 'password', 'First', 'Last')

    payload = requests.get(f'{BASE_URL}/channels/listall/v2', params={'token': token})

    p = payload.json()
    assert p == {'channels': []}


#feature 2: if token that given in the parameter dose not exist, raise AccessError
def test_listall_sid_validity():

    clear()

    # generate a token that doesn't exist.
    token = user_sign_up('test@gmail.com', 'password', 'First', 'Last')
    requests.post(f'{BASE_URL}/auth/logout/v1', json={'token': token})

    payload = requests.get(f'{BASE_URL}/channels/listall/v2', params={'token': token})

    assert payload.status_code == 403

def test_listall_uid_validity():
    clear()
    #generate a token that the user_id is removed.
    token = user_sign_up('test@gmail.com', 'password', 'First', 'Last')

    #clear again to make the u_id invalid
    clear()

    payload = requests.get(f'{BASE_URL}/channels/listall/v2', params={'token': token})

    assert payload.status_code == 403

#feature 3: test the general functionality of the listall function
def test_listall_general():

    clear()

    token = user_sign_up('test@gmail.com', 'password', 'First', 'Last')
    #create a channel via the token that generated by user_register
    payload_1 = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token,
                                                            'name': 'correct1',
                                                            'is_public': True})
    #create another channel by the same person
    payload_2 = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token,
                                                            'name': 'correct2',
                                                            'is_public': True})
    p1 = payload_1.json()
    p2 = payload_2.json()

    payload_3 = requests.get(f'{BASE_URL}/channels/listall/v2', params={'token': token})
    p3 = payload_3.json()

    assert p3 == {'channels': [
                                {'channel_id': p1['channel_id'],
                                        'name': 'correct1',
                                },
                                {'channel_id': p2['channel_id'],
                                    'name': 'correct2',
                                }
                            ],
                 }

###########################################################################################

## channel/leave/v1

# feature 1: raise access error when channel_id is valid and the authorised user is not a member of the channel
def test_leave_not_member():

    clear()

    token_1 = user_sign_up('test1@gmail.com', 'password1', 'First1', 'Last1')
    token_2 = user_sign_up('test2@gmail.com', 'password2', 'First2', 'Last2')
    payload = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token_1,
                                                            'name': 'correct1',
                                                            'is_public': True})
    p = payload.json()
    
    r_type = requests.post(f'{BASE_URL}/channel/leave/v1', json={'token': token_2, 'channel_id': p['channel_id']})

    assert r_type.status_code == 403


# feature 2: raise input error when channel_id does not refer to a valid channel
def test_leave_channel_invalid():

    clear()

    token = user_sign_up('test2@gmail.com', 'password2', 'First2', 'Last2')
    #a random invalid channel id
    c_id = 100
    
    r_type = requests.post(f'{BASE_URL}/channel/leave/v1', json={'token': token, 'channel_id': c_id})

    assert r_type.status_code == 400


#feature 3: after successfully call the function, the return type should be an empty dict
def test_leave_check_return():

    clear()

    token = user_sign_up('test1@gmail.com', 'password1', 'First1', 'Last1')
    payload = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token,
                                                            'name': 'correct1',
                                                            'is_public': True})
    p = payload.json()
    
    r_type = requests.post(f'{BASE_URL}/channel/leave/v1', json={'token': token, 'channel_id': p['channel_id']})
    r = r_type.json()

    assert r == {}

# feature 4: raise access error when the toke entered is invalid(u_id or session_id)
'''
def test_leave_uid_validity():
    clear()
    #register a user
    token_1 = user_sign_up('test@gmail.com', 'password', 'First', 'Last')
    
    #use the token to create a channel
    payload_1 = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token_1,
                                                            'name': 'correct1',
                                                            'is_public': True})
    p1 = payload_1.json()
    #create another user
    payload_2 = requests.post(f'{BASE_URL}/auth/register/v2', json= {'email': 'test2@gmail.com',
                                                            'password': 'password2',
                                                            'name_first': 'first2',
                                                            'name_last': 'last2'})
    p2 = payload_2.json()
    token_2 = p2['token']
    u_id_2 = p2['auth_user_id']
    #make this user join the channel
    requests.post(f'{BASE_URL}/channel/join/v2', json={'token': token_2, 'channel_id': p1['channel_id']})
    #remove token_2 user
    requests.post(f'{BASE_URL}/admin/user/remove/v1', json={'token': token_1, 'u_id':u_id_2 })

    r_type = requests.post(f'{BASE_URL}/channel/leave/v1', json={'token': token_2})

    assert r_type.status_code == 403
'''

def test_leave_sid_validity():
    clear()
    token = user_sign_up('test@gmail.com', 'password', 'First', 'Last')
    payload = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token,
                                                            'name': 'correct1',
                                                            'is_public': True})
    p = payload.json()

    requests.post(f'{BASE_URL}/auth/logout/v1', json={'token': token})

    r_type = requests.post(f'{BASE_URL}/channel/leave/v1', json={'token': token, 'channel_id': p['channel_id']})

    assert r_type.status_code == 403
    
    
def test_list_sid_validity():

    clear()

    # generate a token that doesn't exist.
    token = user_sign_up('test@gmail.com', 'password', 'First', 'Last')
    requests.post(f'{BASE_URL}/auth/logout/v1', json={'token': token})

    payload = requests.get(f'{BASE_URL}/channels/list/v2', params={'token': token})

    assert payload.status_code == 403
    
def test_list_uid_validity():
    clear()
    #generate a token that the user_id is removed.
    token = user_sign_up('test@gmail.com', 'password', 'First', 'Last')

    #clear again to make the u_id invalid
    clear()

    payload = requests.get(f'{BASE_URL}/channels/list/v2', params={'token': token})

    assert payload.status_code == 403

