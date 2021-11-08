import pytest

from src.channel import channel_details_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src import config

#Checks if InputError is raised when channel_id does not refer to a valid channel.
def test_details_channel_id_valid():
    clear_v1()

    user = auth_register_v1("test@gmail.com", "password", "First", "Last")
    user_id = user['auth_user_id']

    #No channel names exist that are less that 1 as per channels_create_v1,
    #thus channel_id "" refers to an invalid channel
    with pytest.raises(InputError):
        channel_details_v1(user_id, "")


#Checks if AccessError is raised when channel_id is valid but user is not a member.
def test_details_user_is_member():
    clear_v1()

    user = auth_register_v1("test@gmail.com", "password", "First", "Last")
    user_id = user['auth_user_id']
    user2 = auth_register_v1("test2@gmail.com", "password2", "First2", "Last2")
    user2_id = user2['auth_user_id']
    channel = channels_create_v1(user_id, "Name", False)
    channel_id = channel['channel_id']

    with pytest.raises(AccessError):
        channel_details_v1(user2_id, channel_id)


#Tests if details_v1 returns correct fields for a simple test case.
def test_details_return_types():
    clear_v1()

    user = auth_register_v1("test@gmail.com", "password", "First", "Last")
    user_id = user['auth_user_id']
    channel = channels_create_v1(user_id, "Name", False)
    channel_id = channel['channel_id']

    details = channel_details_v1(user_id, channel_id)
    details_name = details['name']
    details_public = details['is_public']
    details_owners = details['owner_members']
    details_members = details['all_members']
    test_dict = [{
        'u_id': 1,
        'email': "test@gmail.com",
        'name_first': "First",
        'name_last': "Last",
        'handle_str': "firstlast",
        'profile_img_url' : config.url + "static/default.jpg"
    }]

    assert details_name == 'Name'
    assert not details_public
    assert details_owners == test_dict
    assert details_members == test_dict
