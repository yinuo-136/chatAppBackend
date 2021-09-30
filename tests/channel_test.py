import pytest

from src.error import InputError
from src.error import AccessError

from src.auth import auth_register_v1

from src.channels import channels_create_v1

from src.channel import channel_invite_v1
from src.channel import channel_join_v1
from src.other import clear_v1

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

def test_channel_inv__user_id_valid():

    register_id_return = auth_register_v1("test@gmail.com", "password", "First", "Last")
    auth_u_id = register_id_return['auth_user_id']

    return_c_id = channels_create_v1(auth_u_id, "TestChannel", False)
    c_id = return_c_id['channel_id']

    unregistered_u_id = 999

    with pytest.raises(InputError):
        channel_invite_v1(auth_u_id, c_id, unregistered_u_id)




#def test_basic_channel_invite_fail__user_id_invalid():
# channel invite => register user 



