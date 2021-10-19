import requests
import json
from requests.api import request
from src import config
from src.dm import dm_create_v1, dm_list_v1
from src.auth import auth_register_v1
from src.other import clear_v1

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
'''

def test_dm_create__local():

    clear_v1()

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
##################################### END OF dm_create_v1 TESTS


#################################### START OF dm_list_v1 TESTS

def test_local__dm_list():

    clear_v1()

    dct_1 = auth_register_v1("test1@gmail.com", "password", "Nicholas", "Stathakis")
    u_id_1 = dct_1['auth_user_id']

    dct_2 = auth_register_v1("test2@gmail.com", "password", "Zeddy", "Zarnacle")
    u_id_2 = dct_2['auth_user_id']

    dict_dm_id = dm_create_v1(u_id_1, [u_id_2])

    dm_id = dict_dm_id['dm_id']

    assert dm_id == 1

    ret = dm_list_v1(u_id_2)
    dm = ret['dms']

    assert dm == [{'dm_id': 1, 'name': 'nicholasstathakis, zeddyzarnacle'}]


def test_dm_list__success_basic():

    # TODO: Clear, register two users, and create a dm between the two

    my_user_token = "xxx"

    payload = {'token' : my_user_token} 
    payload = json.dumps(payload)

    r = requests.get(BASE_URL + "dm/list/v1", data=payload)

    status_code = r.status_code
    response_dict = json.loads(r.text)

    assert status_code == SUCCESS # aka 200 OK
    assert response_dict == { 'dms' : [{'dm_id': 1, 'name': 'nicholasstathakis, zeddyzarnacle'}] } # NEXT SHOULD BE 2 ID



##################################### END OF dm_list_v1 TESTS


#################################### START OF dm_remove_v1 TESTS

'''
#Remove an existing DM, so all members are no longer in the DM. This can only be done by the original creator of the DM.
'''

def test_dm_remove__error__dm_id_invalid():

    # TODO: Clear, register one user, try remove a random channel

    my_user_token = "xxx"
    invalid_dm_id = 999

    payload = {'token' : my_user_token, 'dm_id' : invalid_dm_id} 
    payload = json.dumps(payload)

    r = requests.delete(BASE_URL + "dm/remove/v1", data=payload)

    status_code = r.status_code

    assert status_code == INPUT_ERROR_CODE


def test_dm_remove__error__user_unauthorised():

    # TODO: Clear, register TWO users

    # CREATE DM
    my_user_token = "xxx"
    other_u_ids = [2]

    payload = {'token' : my_user_token, 'u_ids' : other_u_ids} 
    payload = json.dumps(payload)

    r = requests.post(BASE_URL + "dm/create/v1", data=payload)

    status_code = r.status_code
    response_message = json.loads(r.text)

    dm_id = response_message['dm_id']


    unauthorised_u_id = other_u_ids[0]

    # TODO: Get token of unauthorised u_id

    unauthorised_token = "yyy"

    payload = {'token' : unauthorised_token, 'dm_id' : dm_id} 
    payload = json.dumps(payload)

    r = requests.delete(BASE_URL + "dm/remove/v1", data=payload)

    status_code = r.status_code

    assert status_code == ACCESS_ERROR_CODE
'''