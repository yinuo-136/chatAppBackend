import pytest
import requests
from wrapper.channels_wrappers import clear, user_sign_up, user_create_channel
from wrapper.message_wrappers import send_message, senddm_message, edit_message, share_messages, react_message, unreact_message, pin_message, unpin_message
from wrapper.dm_wrappers import dm_create_wrapper
from wrapper.auth_wrappers import auth_register
from wrapper.channel_wrappers import channel_join, channel_invite
from wrapper.notifications_wrapper import get_notifications
from src.config import url

BASE_URL = url

###############################################################################################################
#notification_get_v1 tests
#feature 1: test successful cases
def test_notification_get_successful_one():
    clear()
    token_1 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')

    payload = get_notifications(token_1)
    assert payload.status_code == 200

def testtest_notification_get_successful_two():
    clear()
    token_1 = user_sign_up('test1@gmail.com', 'password1', 'first1', 'last1')
    r2 = auth_register("test2@gmail.com", "password123", "Johnny", "Sins")
    token_2 = r2.json()['token']
    u_id = r2.json()['auth_user_id']
    c_id_1 = user_create_channel(token_1, 'name', False)
    c_id_2 = user_create_channel(token_1, 'name2', False)
    channel_invite(token_1, c_id_1, u_id)
    channel_invite(token_1, c_id_2, u_id)
    payload = get_notifications(token_2)
    assert payload.status_code == 200 

