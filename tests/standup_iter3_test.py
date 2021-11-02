from typing import Any
import requests
import json
import jwt
from requests.api import request
from src import config
from src.other import clear_v1

from wrapper.standup_wrappers import standup_create_wrapper, standup_is_active_wrapper
from wrapper.auth_wrappers import auth_register
from wrapper.channels_wrappers import user_create_channel
from wrapper.clear_wrapper import clear_http


ACCESS_ERROR = 403
INPUT_ERROR = 400
SUCCESS = 200

'''
Parameters:{ token, channel_id, length }
'''

def test_standup_start__success__basic():

    # Clear

    clear_http()

    # Register a user


    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']

    # create a channel


    c_id1 = user_create_channel(token, "testchannel1", False)


    # start a standup

    standup_response = standup_create_wrapper(token, c_id1, 60) #create for 60 seconds

    # check it returns 200 OK and a time_finish

    status_code = standup_response.status_code
    response_body = json.loads(standup_response.text)


    assert status_code == SUCCESS
    assert len(response_body) == 1 #it contains one field `time_finish`


def test_standup_start__fail__channel_id_invalid():

    # Clear

    clear_http()

    # Register a user


    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']

    # start a standup with INVALID ID

    invalid_c_id = 9999

    standup_response = standup_create_wrapper(token, invalid_c_id, 60) #create for 60 seconds

    # check it returns 200 OK and a time_finish

    status_code = standup_response.status_code

    assert status_code == INPUT_ERROR



def test_standup_start__fail__length_negative_int():

    # Clear

    clear_http()

    # Register a user


    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']

    # create a channel


    c_id1 = user_create_channel(token, "testchannel1", False)


    # start a standup

    standup_response = standup_create_wrapper(token, c_id1, -1) # invalid -1 second time for standup

    # check it returns 200 OK and a time_finish

    status_code = standup_response.status_code


    assert status_code == INPUT_ERROR




def test_standup_start__fail__active_standup_already():

    # Clear

    clear_http()

    # Register a user


    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']

    # create a channel


    c_id1 = user_create_channel(token, "testchannel1", False)


    # start a standup

    standup_create_wrapper(token, c_id1, 60) #create for 60 seconds
    standup_response = standup_create_wrapper(token, c_id1, 60) #create for 60 seconds

    # check it returns 200 OK and a time_finish

    status_code = standup_response.status_code


    assert status_code == INPUT_ERROR


#################### BEGIN OF STANDUP_ACTIVE


def test_standup_active__success_basic():

    # Clear

    clear_http()

    # Register a user


    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']

    # create a channel


    c_id1 = user_create_channel(token, "testchannel1", False)


    # start a standup

    standup_create_wrapper(token, c_id1, 60) #create for 60 seconds

    # test if standup active, should be YES!

    response_body = standup_is_active_wrapper(token, c_id1)

    status_code = response_body.status_code
    response_dict = json.loads(response_body.text)

    assert status_code == SUCCESS
    assert response_dict['is_active'] == True



#################### BEGIN OF standup/send/v1



def test_standup_send__success__basic():

    #clear

    clear_http()

    # Register a user


    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']

    # create a channel


    c_id1 = user_create_channel(token, "testchannel1", False)


    # start a standup

    standup_create_wrapper(token, c_id1, 60) #create for 60 seconds

    # send message to standup

    r = standup_send_wrapper(token, c_id1, "this is a test message")

    # check 200 OK

    status_code = r.status_code
    response_body = json.loads(r.text)

    assert status_code == SUCCESS
    assert response_body == {}