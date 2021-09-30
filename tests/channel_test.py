import pytest

from src.error import InputError
from src.error import AccessError

from src.auth import auth_register_v1

from src.channels import channels_create_v1

from src.channel import channel_invite_v1
from src.channel import channel_join_v1
from src.other import clear_v1



@pytest.fixture
def clear__register_user__create_channel():

    clear_v1()

    register_id_return = auth_register_v1("test@gmail.com", "password", "First", "Last")
    auth_u_id = register_id_return['auth_user_id']

    return_c_id = channels_create_v1(auth_u_id, "TestChannel", False)
    c_id = return_c_id['channel_id']

    return [auth_u_id, c_id]


@pytest.fixture
def clear__register_two_users():

    clear_v1()

    register_id_return_1 = auth_register_v1("test1@gmail.com", "password", "First", "Last")
    auth_u_id_1 = register_id_return_1['auth_user_id']

    register_id_return_2 = auth_register_v1("test2@gmail.com", "password", "First", "Last")
    auth_u_id_2 = register_id_return_2['auth_user_id']

    return [auth_u_id_1, auth_u_id_2]



@pytest.fixture
def clear__register_two_users__create_channel():

    clear_v1()

    register_id_return_1 = auth_register_v1("test1@gmail.com", "password", "First", "Last")
    auth_u_id_1 = register_id_return_1['auth_user_id']

    register_id_return_2 = auth_register_v1("test2@gmail.com", "password", "First", "Last")
    auth_u_id_2 = register_id_return_2['auth_user_id']

    return_c_id = channels_create_v1(auth_u_id_1, "TestChannel", False)
    c_id = return_c_id['channel_id']

    return [auth_u_id_1, auth_u_id_2, c_id]



################ START BLACKBOX


def test_channel_inv__user_id_valid(clear__register_user__create_channel):

    auth_u_id, c_id = clear__register_user__create_channel

    unregistered_u_id = 999

    with pytest.raises(InputError):
        channel_invite_v1(auth_u_id, c_id, unregistered_u_id)



def test_channel_inv__channel_id_invalid(clear__register_two_users):

    auth_u_id_1, auth_u_id_2 = clear__register_two_users

    invalid_channel = 999

    with pytest.raises(InputError):
        channel_invite_v1(auth_u_id_1, invalid_channel, auth_u_id_2)



def test_channel_inv__u_id_already_member(clear__register_two_users):

    auth_u_id_1, auth_u_id_2 = clear__register_two_users

    return_c_id = channels_create_v1(auth_u_id_1, "TestChannel", False)
    c_id = return_c_id['channel_id']


    channel_invite_v1(auth_u_id_1, c_id, auth_u_id_2)

    with pytest.raises(InputError):
        channel_invite_v1(auth_u_id_1, c_id, auth_u_id_2)


def test_channel_invite__channel_id_valid__auth_not_member(clear__register_two_users__create_channel):

    u_id_1, u_id_2, c_id = clear__register_two_users__create_channel


    new_user = auth_register_v1("random@gmail.com", "password", "First", "Last")
    new_u_id = new_user['auth_user_id']

    with pytest.raises(AccessError):
        channel_invite_v1(new_u_id, c_id, u_id_2)

'''
`channel inv`
Check auth user id is valid 
Check channel id is valid
Check u_id is valid 
Check u_id is already member of channel details v1 (shouldnt already be member) [AccessError]
Check whether auth user id is apart of channel

`channel join`
Check for valid user id
Valid channel id
Check for private channel access [AccessError]
 '''

'''

Parameters:{ 
    auth_user_id = the user ID of the user who is making the request, 
    channel_id = unique id of channel which user is being invited to, 
    u_id =  user ID of user who is being invited}

'''