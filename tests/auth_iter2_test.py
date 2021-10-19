import pytest
import jwt
import requests
import uuid
import json
from wrapper.auth_wrappers import auth_register, auth_login, auth_logout
from wrapper.clear_wrapper import clear_http
from src import config

def test_basic_auth_register():
    
    r = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    
    resp = r.json()
    
    assert type(resp['token']) is str
    assert resp['auth_user_id'] == 1
    
    clear_http()
    
def test_basic_auth_login_logout():
    
    auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    r = auth_login("email@gmail.com", "password123")
    
    resp = r.json()
    
    assert type(resp['token']) is str
    assert resp['auth_user_id'] == 1
    
    
    r1 = auth_logout(resp['token'])
     
    assert r1.json() == {}
    
    clear_http()
    
    
