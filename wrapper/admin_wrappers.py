import pytest
import requests
import uuid
import json
from src import config

def admin_remove(token, u_id):
    payload = {
        'token' : token,
        'u_id' : u_id
    }
    
    return requests.delete(config.url + "admin/user/remove/v1", json = payload)
    

def admin_permission(token, u_id, permission_id):
    payload = {
        'token' : token,
        'u_id' : u_id,
        'permission_id' : permission_id
    } 
    
    return requests.post(config.url + "admin/userpermission/change/v1", json = payload)

