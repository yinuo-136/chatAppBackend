import pytest

from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import AccessError, InputError
from src.other import clear_v1

# channels_create_v1 feature 1: length of name is less than 1 or more than 20 characters, 
# if it fails the rule, raise an InputError.
def test_user_name():

    clear_v1()

    u_id = auth_register_v1("test@gmail.com", "password", "First", "Last")

    #check if the error raises if length of the name is less than 1
    with pytest.raises(InputError):
        channels_create_v1(u_id, "", False)
    
    #chcek if the error raises if length of the name is more than 20
    with pytest.raises(InputError):
        channels_create_v1(u_id, "abcdefghijklmnopqrstuvwxyz", False) 

# channels_create_v1 feature 2: if the user didn't input the correct u_id（not exist), raise an 
# AccessError.
def test_uid_validity():

    clear_v1()

    u_id = 12

    with pytest.raises(AccessError):
        channels_create_v1(u_id, "correct_name", False)

# channels_create_v1 feature 3: if both InputError(caused by name) and AccessError(caused by u_id)
#  should've raised, raised AccessError
def test_error_raised():
    
    clear_v1()

    u_id = 12

    with pytest.raises(AccessError):
        channels_create_v1(u_id,"", False)

# channels_create_v1 feature 4:  eachtime the channel_id that created by the function should
#  be unique.
def test_channel_id_unique():

    clear_v1()

    u_id = auth_register_v1("test@gmail.com", "password", "First", "Last")
    c_id_1 = channels_create_v1(u_id, "correct_name", False)
    c_id_2 = channels_create_v1(u_id, "correct_name_1", False)
    assert c_id_1 != c_id_2
