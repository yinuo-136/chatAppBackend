import pytest
import requests
import json
from src import config

def auth_register(email, password, name_first, name_last):
    payload = {'email' : email, 
        'password' : password, 
        'name_first' : name_first, 
        'name_last' : name_last}
    
    return requests.post(config.url + "auth/register/v2", json = payload)   
    
def auth_login(email, password):
    payload = {'email' : email, 'password' : password}

    return requests.post(config.url + "auth/login/v2", json = payload)
    
def auth_logout(token):
    
    payload = {'token' : token}
    
    return requests.post(config.url + "auth/logout/v1", json = payload)    

