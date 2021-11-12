import pytest
import requests
from time import sleep
from datetime import datetime, timezone
from wrapper.clear_wrapper import clear_http
from wrapper.auth_wrappers import auth_register
from wrapper.user_wrappers import users_stats
from wrapper.channel_wrappers import channel_join
from wrapper.channels_wrappers import user_create_channel
from wrapper.dm_wrappers import dm_create_wrapper, dm_remove_wrapper
from wrapper.message_wrappers import send_message, sendlater_ch, remove_messages


#utilisation_rate calc = num_users_who_have_joined_at_least_one_channel_or_dm / num_users

@pytest.fixture
def current_time():    
    dt = datetime.now(timezone.utc)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    return int(timestamp)   
    

def test_users_stats_new_user(current_time):
    clear_http()	
	
    r = auth_register("test_1@gmail.com", "password", "John", "Smith")
    token = r.json()['token']
	
    r1 = users_stats(token)

    assert r1.json() == {'workspace_stats' : {'channels_exist': [{'num_channels_exist': 0, 'time_stamp': current_time}],
                        'dms_exist': [{'num_dms_exist': 0, 'time_stamp': current_time}],
                        'messages_exist': [{'num_messages_exist': 0, 'time_stamp': current_time}],
                        'utilization_rate' : 0.0}}

def test_users_stats_create_channel(current_time):

    clear_http()
	  
    r = auth_register("test_1@gmail.com", "password", "John", "Smith")
    token = r.json()['token']
    
    
    user_create_channel(token, "channel_1", True)
   
    
    r1 = users_stats(token)
    
    assert r1.json()['workspace_stats']['channels_exist'][-1]['num_channels_exist'] == 1 
    assert r1.json()['workspace_stats']['utilization_rate'] == 1.0
                        
                   
def test_users_dm_createremove(current_time):
    clear_http()
    
    r1 = auth_register("test@gmail.com", "password123", "john", "smith")
    r2 = auth_register("somerandom@gmail.com", "password123", "smith", "john")
    token = r1.json()['token']
    
    data1 = r1.json()
    data2 = r2.json()


    my_user_token = data1['token']
    valid_other_id = data2['auth_user_id']
    
    dm_create_wrapper(my_user_token, [valid_other_id])
    
    r3 = users_stats(token)
    
    assert r3.json()['workspace_stats']['dms_exist'][-1]['num_dms_exist'] == 1 
    assert r3.json()['workspace_stats']['utilization_rate'] == 1.0
    
    dm_remove_wrapper(my_user_token, 1)
    
    r4 = users_stats(token)
    
    assert r4.json()['workspace_stats']['dms_exist'][-1]['num_dms_exist'] == 0 
    assert r4.json()['workspace_stats']['utilization_rate'] == 0.0 
 
def test_send_message_remove(current_time):   
    clear_http()
    
    r = auth_register("test_1@gmail.com", "password", "John", "Smith")
    token = r.json()['token']
    
    user_create_channel(token, "channel_1", True)
    
    send_message(token, 1, "cool message")
    
    r1 = users_stats(token)

    assert r1.json()['workspace_stats']['messages_exist'][-1]['num_messages_exist'] == 1
    assert r1.json()['workspace_stats']['utilization_rate'] == 1.0

    remove_messages(token, 1)

    r4 = users_stats(token)
    
    assert r4.json()['workspace_stats']['messages_exist'][-1]['num_messages_exist'] == 0 
    assert r4.json()['workspace_stats']['utilization_rate'] == 1.0 
    
def test_stats_sendlater(current_time):
    clear_http()
    
    r = auth_register("test_1@gmail.com", "password", "John", "Smith")
    token = r.json()['token']
    
    user_create_channel(token, "channel_1", True)
    
    sendlater_ch(token, 1, "cool message", current_time + 3)
    
    sleep(3)
    
    r1 = users_stats(token)

    assert r1.json()['workspace_stats']['messages_exist'][-1]['num_messages_exist'] == 1
    assert r1.json()['workspace_stats']['messages_exist'][-1]['time_stamp'] == current_time + 3
    assert r1.json()['workspace_stats']['utilization_rate'] == 1.0
    
def test_utilization_rate():
    clear_http()
    
    r = auth_register("test_1@gmail.com", "password", "John", "Smith")
    token = r.json()['token']
    u_id1 = r.json()['auth_user_id']
    
    user_create_channel(token, "channel_1", True)
    
    r2 = auth_register("test_2@gmail.com", "password", "New", "Guy")
    token2 = r2.json()['token']
    u_id2 = r2.json()['auth_user_id']
    
    channel_join(token2, 1)
    
    user_create_channel(token, "channel_2", True)  
    
    r3 = auth_register("test_3@gmail.com", "password", "Bromandude", "Dudemanbro")
    token3 = r3.json()['token']

    dm_create_wrapper(token3, [u_id1, u_id2]) 
    
    r4 = auth_register("test_4@gmail.com", "password", "Coolest", "Member")
    u_id4 = r4.json()['auth_user_id']

    dm_create_wrapper(token3, [u_id1, u_id4]) 
    
    r5 = users_stats(token)
    assert r5.json()['workspace_stats']['utilization_rate'] == 1.0


