import pytest
import requests
from datetime import datetime, timezone
from wrapper.clear_wrapper import clear_http
from wrapper.auth_wrappers import auth_register
from wrapper.user_wrappers import users_stats
from wrapper.channels_wrappers import user_create_channel
from wrapper.dm_wrappers import dm_create_wrapper, dm_remove_wrapper


#utilisation_rate calc = num_users_who_have_joined_at_least_one_channel_or_dm / num_users

def test_users_stats_new_user():
    clear_http()
	
	
    dt = datetime.now(timezone.utc)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    current_time = int(timestamp)

	
	
    r = auth_register("test_1@gmail.com", "password", "John", "Smith")
    token = r.json()['token']
	
    r1 = users_stats(token)

    assert r1.json() == {'workspace_stats' : {'channels_exist': [{'num_channels_exist': 0, 'time_stamp': current_time}],
                        'dms_exist': [{'num_dms_exist': 0, 'time_stamp': current_time}],
                        'messages_exist': [{'num_messages_exist': 0, 'time_stamp': current_time}],
                        'utilization_rate' : 0.0}}
'''
def test_users_stats_create_channel():

    clear_http()
	
    dt = datetime.now(timezone.utc)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    current_time = int(timestamp)
    
    r = auth_register("test_1@gmail.com", "password", "John", "Smith")
    token = r.json()['token']
    
    
    user_create_channel(token, "channel_1", True)
   
    
    r1 = users_stats(token)
    
    assert r1.json() == {'workspace_stats' : {'channels_exist': [{'num_channels_exist': 1, 'time_stamp': current_time}],
                        'dms_exist': [{'num_dms_exist': 0, 'time_stamp': current_time}],
                        'messages_exist': [{'num_messages_exist': 0, 'time_stamp': current_time}],
                       'utilization_rate' : 1.0}}
                        
                   
def test_users_dm_create():
    clear_http()
    
    dt = datetime.now(timezone.utc)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    current_time = int(timestamp)
    
    r1 = auth_register("test@gmail.com", "password123", "john", "smith")
    r2 = auth_register("somerandom@gmail.com", "password123", "smith", "john")
    token = r1.json()['token']
    
    r3 = users_stats(token)


    data1 = r1.json()
    data2 = r2.json()


    my_user_token = data1['token']
    valid_other_id = data2['auth_user_id']
    
    r = dm_create_wrapper(my_user_token, [valid_other_id])
    dm_create_wrapper(my_user_token, [valid_other_id])
    
    assert r3.json() == {'workspace_stats' : {'channels_exist': [{'num_channels_exist': 0, 'time_stamp': current_time}],
                        'dms_exist': [{'num_dms_exist': 1, 'time_stamp': current_time}],
                        'messages_exist': [{'num_messages_exist': 0, 'time_stamp': current_time}],
                        'utilization_rate' : 1.0}}
    

'''
    


