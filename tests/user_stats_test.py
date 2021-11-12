import pytest
import requests
from time import sleep
from datetime import datetime, timezone
from wrapper.clear_wrapper import clear_http
from wrapper.auth_wrappers import auth_register
from wrapper.user_wrappers import user_stats
from wrapper.channels_wrappers import user_create_channel
from wrapper.channel_wrappers import channel_invite, channel_join, channel_leave
from wrapper.dm_wrappers import dm_create_wrapper, dm_remove_wrapper, dm_leave_wrapper
from wrapper.message_wrappers import send_message, senddm_message, sendlater_ch, sendlater_dm
from wrapper.standup_wrappers import standup_create_wrapper

@pytest.fixture
def time():    
    dt = datetime.now(timezone.utc)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    return int(timestamp)   


def test_stats_new_user(time):
    clear_http()
    
    current_time = time    
    
    r = auth_register("test@gmail.com", "password", "Steven", "Wolfe")
    token = r.json()['token']

    r1 = user_stats(token)

    assert r1.json() == {'channels_joined': [{'num_channels_joined': 0, 'time_stamp': current_time}],
                         'dms_joined': [{'num_dms_joined': 0, 'time_stamp': current_time}],
                         'messages_sent': [{'num_messages_sent': 0, 'time_stamp': current_time}],
                         'involvement_rate' : 0.0}


def test_stats_channel_create_join_leave_invite(time):
    clear_http()
    
    current_time = time    

    user = auth_register("test@gmail.com", "password", "Steven", "Wolfe")
    token = user.json()['token']
    user2 = auth_register("test2@gmail.com", "password", "Johnny", "Sins")
    token2 = user2.json()['token']
    u_id2 = user2.json()['auth_user_id']

    channel_id = user_create_channel(token, "CornHub", True)
    channel_join(token2, channel_id)
    channel_leave(token2, channel_id)
    channel_invite(token, channel_id, u_id2)

    r1 = user_stats(token)
    assert r1.json() == {'channels_joined': [{'num_channels_joined': 0, 'time_stamp': current_time},
                                             {'num_channels_joined': 1, 'time_stamp': current_time}],
                         'dms_joined': [{'num_dms_joined': 0, 'time_stamp': current_time}],
                         'messages_sent': [{'num_messages_sent': 0, 'time_stamp': current_time}],
                         'involvement_rate' : 1.0}   

    r2 = user_stats(token2)
    assert r2.json() == {'channels_joined': [{'num_channels_joined': 0, 'time_stamp': current_time},
                                             {'num_channels_joined': 1, 'time_stamp': current_time},
                                             {'num_channels_joined': 0, 'time_stamp': current_time},
                                             {'num_channels_joined': 1, 'time_stamp': current_time}],
                         'dms_joined': [{'num_dms_joined': 0, 'time_stamp': current_time}],
                         'messages_sent': [{'num_messages_sent': 0, 'time_stamp': current_time}],
                         'involvement_rate' : 1.0} 


def test_stats_dms_create_remove(time):
    clear_http()

    current_time = time    
    
    user = auth_register("test@gmail.com", "password", "Steven", "Wolfe")
    token = user.json()['token']
    user2 = auth_register("test2@gmail.com", "password", "Johnny", "Sins")
    token2 = user2.json()['token']
    u_id2 = user2.json()['auth_user_id']
    user3 = auth_register("test3@gmail.com", "password", "Zhong", "Xina")
    u_id3 = user3.json()['auth_user_id']
    token3 = user3.json()['token']

    dm_create_wrapper(token, [u_id2, u_id3])
    dm_remove_wrapper(token, 1)
    

    r1 = user_stats(token)
    assert r1.json() == {'channels_joined': [{'num_channels_joined': 0, 'time_stamp': current_time}],
                         'dms_joined': [{'num_dms_joined': 0, 'time_stamp': current_time},
                                        {'num_dms_joined': 1, 'time_stamp': current_time},
                                        {'num_dms_joined': 0, 'time_stamp': current_time}],
                         'messages_sent': [{'num_messages_sent': 0, 'time_stamp': current_time}],
                         'involvement_rate' : 0.0}   

    r2 = user_stats(token2)
    assert r2.json() == {'channels_joined': [{'num_channels_joined': 0, 'time_stamp': current_time}],
                         'dms_joined': [{'num_dms_joined': 0, 'time_stamp': current_time},
                                        {'num_dms_joined': 1, 'time_stamp': current_time},
                                        {'num_dms_joined': 0, 'time_stamp': current_time}],
                         'messages_sent': [{'num_messages_sent': 0, 'time_stamp': current_time}],
                         'involvement_rate' : 0.0}

    r3 = user_stats(token3)
    assert r3.json() == {'channels_joined': [{'num_channels_joined': 0, 'time_stamp': current_time}],
                         'dms_joined': [{'num_dms_joined': 0, 'time_stamp': current_time},
                                        {'num_dms_joined': 1, 'time_stamp': current_time},
                                        {'num_dms_joined': 0, 'time_stamp': current_time}],
                         'messages_sent': [{'num_messages_sent': 0, 'time_stamp': current_time}],
                         'involvement_rate' : 0.0}


def test_stats_dms_leave(time):
    clear_http()

    current_time = time    

    user = auth_register("test@gmail.com", "password", "Steven", "Wolfe")
    token = user.json()['token']
    user2 = auth_register("test2@gmail.com", "password", "Johnny", "Sins")
    token2 = user2.json()['token']
    u_id2 = user2.json()['auth_user_id']

    dm_create_wrapper(token, [u_id2])
    dm_leave_wrapper(token2, 1)

    r1 = user_stats(token)
    assert r1.json() == {'channels_joined': [{'num_channels_joined': 0, 'time_stamp': current_time}],
                         'dms_joined': [{'num_dms_joined': 0, 'time_stamp': current_time},
                                        {'num_dms_joined': 1, 'time_stamp': current_time}],
                         'messages_sent': [{'num_messages_sent': 0, 'time_stamp': current_time}],
                         'involvement_rate' : 1.0}   

    r2 = user_stats(token2)
    assert r2.json() == {'channels_joined': [{'num_channels_joined': 0, 'time_stamp': current_time}],
                         'dms_joined': [{'num_dms_joined': 0, 'time_stamp': current_time},
                                        {'num_dms_joined': 1, 'time_stamp': current_time},
                                        {'num_dms_joined': 0, 'time_stamp': current_time}],
                         'messages_sent': [{'num_messages_sent': 0, 'time_stamp': current_time}],
                         'involvement_rate' : 0.0}


def test_stats_messages_send(time):
    clear_http()

    current_time = time    

    user = auth_register("test@gmail.com", "password", "Johnny", "Sins")
    token = user.json()['token']
    user2 = auth_register("test2@gmail.com", "password", "Zhong", "Xina")
    token2 = user2.json()['token']
    u_id2 = user2.json()['auth_user_id']

    channel_id = user_create_channel(token, "CornHub", True)
    send_message(token, channel_id, "Hi, engineer, doctor, dentist, teacher, pizza delivery guy... here.")
    dm_create_wrapper(token, [u_id2])
    senddm_message(token2, 1, "Bing Chilling")
    sendlater_ch(token, channel_id, "Hello", current_time + 1)
    sendlater_dm(token2, 1, "Lao Gan Ma", current_time + 1)
    sendlater_dm(token2, 1, "Lao Gan Ma", current_time + 1)
    standup_create_wrapper(token, channel_id, 1)
    sleep(1)

    '''
    User:
    Channels = 1
    DMs = 1
    Messages = 3
    
    User2:
    Channels = 0
    DMs = 1
    Messages = 3

    Expected Involvement (7 Denominator)
    Johnny Sins = 5/8
    Zhong Xina = 4/8
    '''

    r1 = user_stats(token)
    assert r1.json() == {'channels_joined': [{'num_channels_joined': 0, 'time_stamp': current_time},
                                             {'num_channels_joined': 1, 'time_stamp': current_time}],
                         'dms_joined': [{'num_dms_joined': 0, 'time_stamp': current_time},
                                        {'num_dms_joined': 1, 'time_stamp': current_time}],
                         'messages_sent': [{'num_messages_sent': 0, 'time_stamp': current_time},
                                           {'num_messages_sent': 1, 'time_stamp': current_time},
                                           {'num_messages_sent': 2, 'time_stamp': current_time + 1},
                                           {'num_messages_sent': 3, 'time_stamp': current_time + 1}],
                         'involvement_rate' : 0.625}


    r2 = user_stats(token2)
    assert r2.json() == {'channels_joined': [{'num_channels_joined': 0, 'time_stamp': current_time}],
                         'dms_joined': [{'num_dms_joined': 0, 'time_stamp': current_time},
                                        {'num_dms_joined': 1, 'time_stamp': current_time}],
                         'messages_sent': [{'num_messages_sent': 0, 'time_stamp': current_time},
                                           {'num_messages_sent': 1, 'time_stamp': current_time},
                                           {'num_messages_sent': 2, 'time_stamp': current_time + 1},
                                           {'num_messages_sent': 3, 'time_stamp': current_time + 1}],
                         'involvement_rate' : 0.5}
