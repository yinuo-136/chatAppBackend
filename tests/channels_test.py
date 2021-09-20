import pytest

from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1

# channels_create_v1 feature 1: length of name is less than 1 or more than 20 characters, 
# if it fails the rule, raise an InputError.
def test_user_name():

    clear_v1()

    u_id = auth_register_v1("test@gmail.com", "password", "First", "Last")

    #check if the error raises if length of the name is less than 1
    with pytest.raises(InputError):
        assert channels_create_v1(u_id, "", False)
    
    #chcek if the error raises if length of the name is more than 20
    with pytest.raises(InputError):
        assert channels_create_v1(u_id, "abcdefghijklmnopqrstuvwxyz", False) 




# channels_create_v1 feature 2:
# channels_create_v1 feature 3:
# channels_create_v1 feature 4: