import pytest

from src.channels import channels_create_v1
from src.channel import channel_messages_v1
from src.auth import auth_register_v1
from src.error import AccessError, InputError
from src.other import clear_v1

#feature 1: raise Accesserror if user_id does not refer to a valid user
def test_user_id_validity_messages():

    clear_v1()

    u_dict = auth_register_v1("test@gmail.com", "password", "First", "Last")
    u_id_exist = u_dict['auth_user_id']
    u_id_not_exist = u_id_exist + 1
    c_dict = channels_create_v1(u_id_exist, "correct_name", False)
    c_id = c_dict['channel_id']
    
    with pytest.raises(AccessError):
        channel_messages_v1(u_id_not_exist, c_id, 0)
    
#feature 2: raise Accesserror if user is not a member in the channel
def test_user_ismember_messages():

    clear_v1()

    u_dict_1 = auth_register_v1("test1@gmail.com", "password", "First", "Last")
    u_id_1 = u_dict_1['auth_user_id']

    u_dict_2 = auth_register_v1("test2@gmail.com", "password", "First", "Last")
    u_id_2 = u_dict_2['auth_user_id']

    c_dict_1 = channels_create_v1(u_id_1, "correct_name", False)
    c_id_1 = c_dict_1['channel_id']

    with pytest.raises(AccessError):
        channel_messages_v1(u_id_2, c_id_1, 0)

#feature 3: raise Inputerror if channel_id is invalid
def test_channel_isvalid_messages():

    clear_v1()

    u_dict_1 = auth_register_v1("test1@gmail.com", "password", "First", "Last")
    u_id_1 = u_dict_1['auth_user_id']

    c_dict_1 = channels_create_v1(u_id_1, "correct_name", False)
    c_id_1 = c_dict_1['channel_id']

    c_id_not_exist = c_id_1 + 1

    with pytest.raises(InputError):
        channel_messages_v1(u_id_1, c_id_not_exist, 0)

#feature 4: raise InputError if start is greater than the total number 
# of messages in the channel
def test_start_isgreat_message():

    clear_v1()

    u_dict_1 = auth_register_v1("test1@gmail.com", "password", "First", "Last")
    u_id_1 = u_dict_1['auth_user_id']

    c_dict_1 = channels_create_v1(u_id_1, "correct_name", False)
    c_id_1 = c_dict_1['channel_id']

    with pytest.raises(InputError):
        channel_messages_v1(u_id_1, c_id_1, 1)

    with pytest.raises(InputError):
        channel_messages_v1(u_id_1, c_id_1, 10)

#feature 5: raise InputError if start is less than zero
def test_start_less_than_zero():

    clear_v1()

    u_dict_1 = auth_register_v1("test1@gmail.com", "password", "First", "Last")
    u_id_1 = u_dict_1['auth_user_id']

    c_dict_1 = channels_create_v1(u_id_1, "correct_name", False)
    c_id_1 = c_dict_1['channel_id']  

    with pytest.raises(InputError):
        channel_messages_v1(u_id_1, c_id_1, -1)

    with pytest.raises(InputError):
        channel_messages_v1(u_id_1, c_id_1, -10)

    with pytest.raises(InputError):
        channel_messages_v1(u_id_1, c_id_1, -100)

#feature 6: return an empty messages list when everything's correct and start is 0
def test_messages_return():

    clear_v1()

    u_dict_1 = auth_register_v1("test1@gmail.com", "password", "First", "Last")
    u_id_1 = u_dict_1['auth_user_id']

    c_dict_1 = channels_create_v1(u_id_1, "correct_name", False)
    c_id_1 = c_dict_1['channel_id']

    assert channel_messages_v1(u_id_1, c_id_1, 0) == { 'messages': [], 'start': 0, 'end': -1}
        
