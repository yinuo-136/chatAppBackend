from typing import Any
from time import sleep
import requests
import json
import jwt
from requests.api import request
from src import config
from src.other import clear_v1

from wrapper.standup_wrappers import standup_create_wrapper, standup_is_active_wrapper, standup_send_wrapper
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

    standup_response = standup_create_wrapper(token, c_id1, 1) #create for 1 seconds
    sleep(1)
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

    standup_response = standup_create_wrapper(token, invalid_c_id, 1) #create for 1 seconds

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

    standup_create_wrapper(token, c_id1, 1) #create for 1 seconds
    standup_response = standup_create_wrapper(token, c_id1, 1) #create for 1 seconds

    # check it returns 200 OK and a time_finish

    status_code = standup_response.status_code


    assert status_code == INPUT_ERROR



def test_standup_create__fail__user_not_member():

   # Clear

    clear_http()

    # Register a user


    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token1 = r1.json()['token']

    r2 = auth_register("test2@gmail.com", "password123", "Nick", "Magalcky")
    token2 = r2.json()['token']

    # create a channel


    c_id1 = user_create_channel(token1, "testchannel1", False)

    # Start standup


    standup_response = standup_create_wrapper(token2, c_id1, 1) #User who is NOT MEMBER start standup
    
    # Other user not in try start standup

    status_code = standup_response.status_code

    assert status_code == ACCESS_ERROR


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

    standup_create_wrapper(token, c_id1, 1) #create for 1 seconds

    # test if standup active, should be YES!

    response_body = standup_is_active_wrapper(token, c_id1)

    status_code = response_body.status_code
    response_dict = json.loads(response_body.text)

    assert status_code == SUCCESS
    assert response_dict['is_active'] == True



def test_standup_active__success__no_standup_active():

    # Clear

    clear_http()

    # Register a user


    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']

    # create a channel


    c_id1 = user_create_channel(token, "testchannel1", False)


    # start a standup

    response_body = standup_is_active_wrapper(token, c_id1) #create for 1 seconds

    status_code = response_body.status_code
    response_dict = json.loads(response_body.text)

    assert status_code == SUCCESS
    assert response_dict['is_active'] == False



def test_standup_active__fail__channel_id_invalid():

    # Clear

    clear_http()

    # Register a user


    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']

    # run standup active method on an invalid channel

    invalid_c_id = 9999

    standup_response = standup_is_active_wrapper(token, invalid_c_id) #create for 1 seconds

    # check it returns 200 OK and a time_finish

    status_code = standup_response.status_code

    assert status_code == INPUT_ERROR



def test_standup_active__fail__user_not_member():

    # Clear

    clear_http()

    # Register a user


    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token1 = r1.json()['token']

    r2 = auth_register("test2@gmail.com", "password123", "Nick", "Magalcky")
    token2 = r2.json()['token']

    # create a channel


    c_id1 = user_create_channel(token1, "testchannel1", False)

    # Start standup


    standup_create_wrapper(token1, c_id1, 1) #User who is NOT MEMBER start standup
    
    # Other user check if standup active

    standup_response = standup_is_active_wrapper(token2, c_id1)

    status_code = standup_response.status_code

    assert status_code == ACCESS_ERROR



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

    standup_create_wrapper(token, c_id1, 1) #create for 1 seconds

    # send message to standup

    r = standup_send_wrapper(token, c_id1, "this is a test message")

    # check 200 OK

    status_code = r.status_code
    response_body = json.loads(r.text)

    assert status_code == SUCCESS
    assert response_body == {}



def test_standup_send__fail__channel_id_invalid():

     # Clear

    clear_http()

    # Register a user


    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']

    # run standup active method on an invalid channel

    invalid_c_id = 9999

    standup_response = standup_send_wrapper(token, invalid_c_id, "hey there") #create for 1 seconds

    # check it returns 200 OK and a time_finish

    status_code = standup_response.status_code

    assert status_code == INPUT_ERROR



def test_standup_send__fail__message_greater_than_thousand_chars():

    #clear

    clear_http()

    # Register a user


    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']

    # create a channel


    c_id1 = user_create_channel(token, "testchannel1", False)


    # start a standup

    standup_create_wrapper(token, c_id1, 1) #create for 1 seconds

    # send message to standup

    r = standup_send_wrapper(token, c_id1, "a" * 1001)

    # check 200 OK

    status_code = r.status_code
   
    assert status_code == INPUT_ERROR
    


def test_standup_send__fail__no_active_standup():


    #clear

    clear_http()

    # Register a user


    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token = r1.json()['token']

    # create a channel


    c_id1 = user_create_channel(token, "testchannel1", False)


    # send message to NON-EXISTENT standup

    r = standup_send_wrapper(token, c_id1, "this standup doesnt exist! hehehhe")

    # check 200 OK

    status_code = r.status_code
   
    assert status_code == INPUT_ERROR




def test_standup_send__fail__user_not_member():

    # Clear

    clear_http()

    # Register a user


    r1 = auth_register("test1@gmail.com", "password123", "John", "Smith")
    token1 = r1.json()['token']

    r2 = auth_register("test2@gmail.com", "password123", "Nick", "Magalcky")
    token2 = r2.json()['token']

    # create a channel


    c_id1 = user_create_channel(token1, "testchannel1", False)

    # Start standup


    standup_create_wrapper(token1, c_id1, 1) #User who is NOT MEMBER start standup
    
    # Other user check if standup active

    standup_response = standup_send_wrapper(token2, c_id1, "im not a member. I should get an access error :(")

    status_code = standup_response.status_code

    assert status_code == ACCESS_ERROR