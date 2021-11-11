import pytest
import requests
from wrapper.clear_wrapper import clear_http
from wrapper.auth_wrappers import auth_register
from wrapper.user_wrappers import users_stats
from wrapper.channels_wrappers import user_create_channel

#utilisation_rate = num_users_who_have_joined_at_least_one_channel_or_dm / num_users

def test_users_stats_new_user():
	clear_http()
	
	r = auth_register("test_1@gmail.com", "password", "John", "Smith")
	token = r.json()['token']
	
	r1 = users_stats(token)
	
	assert r1.json() == {'channels_exist' : 0, 'dms_exist' : 0, 'messages_exist' : 0, 'utilization_rate' : 0}
	
	
def test_users_stats_create_channel():

	clear_http()
	
	r = auth_register("test_1@gmail.com", "password", "John", "Smith")
	token = r.json()['token']
	
	user_create_channel(token, "Channel_1", True)
	
	r1 = users_stats(token)
	
	assert r1.json() == {'channels_exist' : 1, 'dms_exist' : 0, 'messages_exist' : 0, 'utilization_rate' : 1}
