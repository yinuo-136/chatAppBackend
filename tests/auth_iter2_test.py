import pytest
import jwt
import requests
import uuid
import json
from tests.auth_wrappers import auth_register, auth_login, auth_logout
from src import config

# ADD CLEAR() TO EACH TEST

def test_basic_auth_register():
    
    r = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    
    resp = r.json()
    
    assert type(resp['token']) is str
    assert resp['auth_user_id'] == 1
    
def test_basic_auth_login_logout():

    r = auth_login("email@gmail.com", "password123")
    
    resp = r.json()
    
    assert type(resp['token']) is str
    assert resp['auth_user_id'] == 1
    
    token = jwt.decode(resp['token'], config.SECRET, algorithms=["HS256"])
    
    r1 = auth_logout(1, token['session_id'])
     
    assert r1.json() == {}
    
    
