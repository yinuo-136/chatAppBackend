import pytest

from src.error import InputError
from src.error import AccessError
import src.data_store 
import src.error
from src.channel import channel_invite_v1
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


#def test_basic_channel_invite_fail__user_id_invalid():
# channel invite => register user 



