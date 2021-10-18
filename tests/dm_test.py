import pytest
import requests
import json
from src import config
from src.dm import dm_create_v1

BASE_URL = config.url
ACCESS_ERROR_CODE = 403
INPUT_ERROR_CODE = 400
# AccessError       code = 403

# InputError        code = 400

'''
    u_ids contains the user(s) that this DM is directed to, and will not include the creator. 
    
    The creator is the owner of the DM. name should be automatically generated based on the users that are in this DM. 
    
    The name should be an alphabetically-sorted, comma-and-space-separated list of user handles, e.g. 'ahandle1, bhandle2, chandle3'.
    
    '''

#   InputError when: any u_id in u_ids does not refer to a valid user
def test_dm_create__fail__user_not_valid():

    # payload = {'name' : 'Nick'}
    # payload = json.dumps(payload)
    # r = requests.post(BASE_URL + "names/add", data=payload)
    # assert r.status_code == 200

    payload = {'token' : 'sometoken', "u_ids" : [1, 2, 3, 4]} 
    payload = json.dumps(payload)

    r = requests.post(BASE_URL + "dm/create/v1", data=payload)

    status_code = r.status_code

    assert status_code == INPUT_ERROR_CODE #input-error
