import pytest
import requests


#######################################################################################
# helper functions
BASE_URL = 'http://127.0.0.1:8080'

def clear():
    requests.delete(f'{BASE_URL}/clear/v1')


def user_sign_up(email, password, first, last):
    payload = requests.post(f'{BASE_URL}/auth/register/v2', json= {'email': email,
                                                            'password': password,
                                                            'name_first': first,
                                                            'name_last': last})
    p = payload.json()
    return p['token']

#########################################################################################



## channels/create/v2 tests:

# channels/create/v2 feature 1: length of name is less than 1 or more than 20 characters, 
# if it fails the rule, raise an InputError(error code 400).
def test_user_name_validity_1():

    clear()

    token = user_sign_up('test@gmail.com', 'password', 'First', 'Last')

    payload = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token,
                                                            'name': '',
                                                            'is_public': True})

    #check if the error raises if length of the name is less than 1
    assert payload.status_code == 400


def test_user_name_validity_2(): 
    
    clear()

    token = user_sign_up('test@gmail.com', 'password', 'First', 'Last')

    payload = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token,
                                                            'name': 'a'*50,
                                                            'is_public': True})

    #check if the error raises if length of the name is less than 20
    assert payload.status_code == 400


# channels_create_v1 feature 2: if the user didn't input the correct u_id（not exist), raise an 
# AccessError.
def test_uid_validity():

    clear()

    # a random token that doesn't exist.
    token = "100"

    payload = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token,
                                                            'name': 'correct_name',
                                                            'is_public': True})
    assert payload.status_code == 403


# channels_create_v1 feature 3: if both InputError(caused by name) and AccessError(caused by u_id)
#  should've raised, raised AccessError
def test_which_error_raised():
    
    clear()

    token = "100"

    payload = requests.post(f'{BASE_URL}/channels/create/v2', json={'token': token,
                                                            'name': '',
                                                            'is_public': True})
    assert payload.status_code == 403
    


# channels_create_v1 feature 4:  eachtime the channel_id that created by the function should
#  be unique.
def test_channel_id_unique():

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

    clear_v1()

    u_dict = auth_register_v1("test@gmail.com", "password", "First", "Last")
    u_id = u_dict['auth_user_id']

    all_list = channels_listall_v1(u_id)
    assert all_list == {'channels': []}


#feature 2: if user id that given in the parameter dose not exist, raise AccessError
def test_listall_uid_validity():

    clear_v1()

    u_id = 12 

    with pytest.raises(AccessError):
        channels_listall_v1(u_id)


#feature 3: test the general functionality of the listall function
def test_listall_general():

    clear_v1()

    u_dict_1 = auth_register_v1("test_1@gmail.com", "password", "First", "Last")
    u_id_1 = u_dict_1['auth_user_id']

    u_dict_2 = auth_register_v1("test_2@gmail.com", "password", "First", "Last")
    u_id_2 = u_dict_2['auth_user_id']

    c_dict_1 = channels_create_v1(u_id_1, 'name_1', False)
    c_dict_2 = channels_create_v1(u_id_2, 'name_2', True)

    c_id_1 = c_dict_1['channel_id']
    c_id_2 = c_dict_2['channel_id']

    assert channels_listall_v1(u_id_1) == {
                                        'channels': [
                                            {'channel_id': c_id_1,
                                             'name': 'name_1',
                                            },
                                            {'channel_id': c_id_2,
                                             'name': 'name_2',
                                            }
                                         ],
                                    }
    
    assert channels_listall_v1(u_id_2) == {
                                        'channels': [
                                            {'channel_id': c_id_1,
                                             'name': 'name_1',
                                            },
                                            {'channel_id': c_id_2,
                                             'name': 'name_2',
                                            }
                                         ],
                                    }


#test user id validity check in list function
def test_list_ui_validity():
    clear_v1()
    u_id = 12 
    with pytest.raises(AccessError):
        channels_list_v1(u_id)

    

