import pytest
import requests
import json
from src import config

def user_profile(token, u_id):
    payload = {'token' : token, 'u_id' : u_id}
    
    return requests.get(config.url + "user/profile/v1", params = payload)  
    
def list_users(token):
    payload = {'token' : token}
    
    return requests.get(config.url + "users/all/v1", params = payload)  
    
    
def set_name(token, name_first, name_last):
    
    payload = {
        'token' : token,
        'name_first' : name_first,
        'name_last' : name_last
    }
    
    return requests.put(config.url + "user/profile/setname/v1", json = payload)  

def set_email(token, email):
    
    payload = {'token' : token, 'email' : email}
    
    return requests.put(config.url + "user/profile/setemail/v1", json = payload)  

def set_handle(token, handle_str):
    
    payload = {'token' : token, 'handle_str' : handle_str}
    
    return requests.put(config.url + "user/profile/sethandle/v1", json = payload)  
    
def upload_photo(token, img_url, x1, y1, x2, y2):
    
    payload = {
        'token' : token,
        'img_url' : img_url,
        'x_start' : x1,
        'y_start' : y1,
        'x_end' : x2,
        'y_end' : y2
    }
    
    return requests.post(config.url + "user/profile/uploadphoto/v1", json = payload)  

def user_stats(token):
    payload = {'token' : token}

    return requests.get(config.url + "user/stats/v1", params = payload)

def users_stats(token):
    payload = {'token' : token}
    
    return requests.get(config.url + "users/stats/v1", params = payload)
