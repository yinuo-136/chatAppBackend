import pytest
import requests
import jwt
import json
from src import config

def user_profile(user_id):
    
    pretoken = {
        'user_id' : user_id,
        'session_id' : 'assume_this_is_correct'
    }
    
    token = jwt.encode(pretoken, config.SECRET, algorithm = 'HS256')
    
    payload = {'token' : token}
    
    return requests.get(config.url + "user/profile/v1", params = payload)  
    
    
def set_name(user_id, name_first, name_last):
    pretoken = {
        'user_id' : user_id,
        'session_id' : 'assume_this_is_correct'
    }
    
    token = jwt.encode(pretoken, config.SECRET, algorithm = 'HS256')
    
    payload = {
        'token' : token,
        'name_first' : name_first,
        'name_last' : name_last
    }
    
    return requests.put(config.url + "user/profile/setname/v1", json = payload)  

def set_email(user_id, email):
    pretoken = {
        'user_id' : user_id,
        'session_id' : 'assume_this_is_correct'
    }
    
    token = jwt.encode(pretoken, config.SECRET, algorithm = 'HS256')
    
    payload = {'token' : token, 'email' : email}
    
    return requests.put(config.url + "user/profile/setemail/v1", json = payload)  

def set_handle(user_id, handle_str):
    pretoken = {
        'user_id' : user_id,
        'session_id' : 'assume_this_is_correct'
    }
    
    token = jwt.encode(pretoken, config.SECRET, algorithm = 'HS256')
    
    payload = {'token' : token, 'handle_str' : handle_str}
    
    return requests.put(config.url + "user/profile/sethandle/v1", json = payload)  


