import pytest

from src.channels import channels_create_v1, channels_listall_v1
from src.auth import auth_register_v1
from src.error import AccessError, InputError
from src.other import clear_v1
from src.data_store import data_store

#########################################################################################

## channels_create_v1 tests:

# channels_create_v1 feature 1: length of name is less than 1 or more than 20 characters, 
# if it fails the rule, raise an InputError.
def test_user_name_validity():

    clear_v1()

    u_dict = auth_register_v1("test@gmail.com", "password", "First", "Last")
    u_id = u_dict['auth_user_id']

    #check if the error raises if length of the name is less than 1
    with pytest.raises(InputError):
        channels_create_v1(u_id, "", False)
    
    #chcek if the error raises if length of the name is more than 20
    with pytest.raises(InputError):
        channels_create_v1(u_id, "a" * 21, False) 


# channels_create_v1 feature 2: if the user didn't input the correct u_id（not exist), raise an 
# AccessError.
def test_uid_validity():

    clear_v1()

    # a random number that doesn't exist.
    u_id = 12

    with pytest.raises(AccessError):
        channels_create_v1(u_id, "correct_name", False)

# channels_create_v1 feature 3: if both InputError(caused by name) and AccessError(caused by u_id)
#  should've raised, raised AccessError
def test_which_error_raised():
    
    clear_v1()

    u_id = 12

    with pytest.raises(AccessError):
        channels_create_v1(u_id,"", False)
    
    with pytest.raises(AccessError):
        channels_create_v1(u_id, "a" * 38, False)


# channels_create_v1 feature 4:  eachtime the channel_id that created by the function should
#  be unique.
def test_channel_id_unique():

    clear_v1()

    u_dict = auth_register_v1("test@gmail.com", "password", "First", "Last")
    u_id = u_dict['auth_user_id']
    c_dict_1 = channels_create_v1(u_id, "correct_name", False)
    c_dict_2 = channels_create_v1(u_id, "correct_name_1", False)
    c_id_1 = c_dict_1['channel_id']
    c_id_2 = c_dict_2['channel_id']
    assert c_id_1 != c_id_2

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


#test list basic functionality
def test_list_general():
    clear_v1()
    store = data_store.get()
    current_channel = store['channels'].get(channel_id)

    u_dict_1 = auth_register_v1("test_1@gmail.com", "password", "First", "Last")
    u_id_1 = u_dict_1['auth_user_id']
    #u_id_1 is a owner of channel 
    current_channel[3].append(u_id_1)

    u_dict_2 = auth_register_v1("test_2@gmail.com", "password", "First", "Last")
    u_id_2 = u_dict_2['auth_user_id']
    #u_id_2 is a member of channel
    current_channel[4].append(u_id_2)

    c_dict_1 = channels_create_v1(u_id_1, 'name_1', True)
    c_dict_2 = channels_create_v1(u_id_2, 'name_2', True)

    c_id_1 = c_dict_1['channel_id']
    c_id_2 = c_dict_2['channel_id']
    
    
    assert channels_list_v1(u_id_1) == {
                                        'channels': [
                                            {'channel_id': c_id_1,
                                             'name': 'name_1',
                                            }
                                         ],
                                    }

    assert channels_list_v1(u_id_2) == {
                                        'channels': [ 
                                            {'channel_id': c_id_2,
                                             'name': 'name_2',
                                            }
                                         ],
                                    }



############################################################

    

