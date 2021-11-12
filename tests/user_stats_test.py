import pytest
import requests
from datetime import datetime, timezone
from wrapper.clear_wrapper import clear_http
from wrapper.auth_wrappers import auth_register
from wrapper.user_wrappers import user_stats
from wrapper.channels_wrappers import user_create_channel

def test_stats_new_user():
    clear_http()

    dt = datetime.now(timezone.utc)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    current_time = int(timestamp)

    r = auth_register("test@gmail.com", "password", "Steven", "Wolfe")
    token = r.json()['token']

    r1 = user_stats(token)

    assert r1.json() == {'channels_joined': [{'num_channels_joined': 0, 'time_stamp': current_time}],
                        'dms_joined': [{'num_dms_joined': 0, 'time_stamp': current_time}],
                        'messages_sent': [{'num_messages_sent': 0, 'time_stamp': current_time}],
                        'involvement_rate' : 0.0}

# def test_stats_channel_join():
#     clear_http()

#     r = auth_register("test@gmail.com", "password", "Steven", "Wolfe")
#     token = r.json()['token']
#     user_create_channel(token, "CornHub", True)

#     r1 = user_stats(token)

#     assert r1.json() == {'channels_joined' : 1, 'dms_joined' : 0, 'messages_sent' : 0,'involvement_rate' : 1.0}

#timestamps
