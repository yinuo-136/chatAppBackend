import pytest
import requests
import json
from src import config

def test_basic_auth_register():
    '''
    A simple test to check auth_register
    '''
    payload = {'email' : 'email@gmail.com', 
        'password' : 'password123', 
        'name_first' : 'Jayden', 
        'name_last' : 'Matthews'}
    
    payload = json.dumps(payload)
    
    r = requests.post(config.url + "auth/register/v2", data = payload)
    
    print(json.loads(r.text))
    
    assert r.status_code == 200
    
    assert json.loads(r.text) == {'token' : '1', 'auth_user_id' : 1}
