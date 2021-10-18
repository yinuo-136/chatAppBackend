import pytest
import requests
import json
from src import config
from src.dm import dm_create_v1
from src.auth import auth_register_v1
from src.data_store import data_store

BASE_URL = config.url


# Status code constants
ACCESS_ERROR_CODE = 403
INPUT_ERROR_CODE = 400
SUCCESS = 200
# AccessError       code = 403
# InputError        code = 400

'''
    u_ids contains the user(s) that this DM is directed to, and will not include the creator. 
    
    The creator is the owner of the DM. name should be automatically generated based on the users that are in this DM. 
    
    The name should be an alphabetically-sorted, comma-and-space-separated list of user handles, e.g. 'ahandle1, bhandle2, chandle3'.
    
    '''


def test_dm_create__local():

    dct_1 = auth_register_v1("test1@gmail.com", "password", "Nicholas", "Stathakis")
    u_id_1 = dct_1['auth_user_id']

    dct_2 = auth_register_v1("test2@gmail.com", "password", "Zeddy", "Zarnacle")
    u_id_2 = dct_2['auth_user_id']

    dict_dm_id = dm_create_v1(u_id_1, [u_id_2])

    dm_id = dict_dm_id['dm_id']

    assert dm_id == 1



#   InputError when: any u_id in u_ids does not refer to a valid user
def test_dm_create__fail__user_not_valid():

    #TODO: clear, register a user, then call the function with user token and invalid_id

    my_user_token = "xxx"
    invalid_user_id = 99


    payload = {'token' : my_user_token, 'u_ids' : [invalid_user_id]} 
    payload = json.dumps(payload)

    r = requests.post(BASE_URL + "dm/create/v1", data=payload)

    status_code = r.status_code

    assert status_code == INPUT_ERROR_CODE #input-error


#successful dm creation
def test_dm_create__success_basic():

    # TODO: clear, register two users, then post

    my_user_token = "xxx"
    valid_other_id = 1


    payload = {'token' : my_user_token, 'u_ids' : [valid_other_id]} 
    payload = json.dumps(payload)

    r = requests.post(BASE_URL + "dm/create/v1", data=payload)

    status_code = r.status_code
    response_dict = json.loads(r.text)

    assert status_code == SUCCESS # aka 200 OK
    assert response_dict == { 'dm_id' : 1 } # should start at 1


def test_dm_create__success__double_dm():

    # TODO: clear, register two users


    ############################ FIRST DM

    my_user_token = "xxx"
    valid_other_id = 1

    payload = {'token' : my_user_token, 'u_ids' : [valid_other_id]} 
    payload = json.dumps(payload)

    r = requests.post(BASE_URL + "dm/create/v1", data=payload)

    status_code = r.status_code
    response_dict = json.loads(r.text)

    assert status_code == SUCCESS # aka 200 OK
    assert response_dict == { 'dm_id' : 1 } # should start at 1


    ################################# SECOND DM

    my_user_token = "yyy"
    valid_other_id = 2

    payload = {'token' : my_user_token, 'u_ids' : [valid_other_id]} 
    payload = json.dumps(payload)

    r = requests.post(BASE_URL + "dm/create/v1", data=payload)

    status_code = r.status_code
    response_dict = json.loads(r.text)

    assert status_code == SUCCESS # aka 200 OK
    assert response_dict == { 'dm_id' : 2 } # NEXT SHOULD BE 2 ID


#Note: cannot test that name of DM will be alphabetically sorted as that would break blackbox