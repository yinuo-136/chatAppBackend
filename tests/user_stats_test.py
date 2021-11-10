import pytest
import requests
from wrapper.clear_wrapper import clear_http
from wrapper.auth_wrappers import auth_register
from wrapper.user_wrappers import user_stats
from wrapper.channels_wrappers import user_create_channel

def test_stats_new_user():
    clear_http()

    r = auth_register("test@gmail.com", "password", "Steven", "Wolfe")
    token = r.json()['token']

    r1 = user_stats(token)

    assert r1.json() == {'channels_joined' : 0, 'dms_joined' : 0, 'messages_sent' : 0,'involvement_rate' : 0}

def test_stats_channel_join():
    clear_http()

    r = auth_register("test@gmail.com", "password", "Steven", "Wolfe")
    token = r.json()['token']
    user_create_channel(token, "CornHub", True)

    r1 = user_stats(token)

    assert r1.json() == {'channels_joined' : 1, 'dms_joined' : 0, 'messages_sent' : 0,'involvement_rate' : 1}
