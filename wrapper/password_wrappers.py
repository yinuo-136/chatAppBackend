import requests
from src import config

def password_request(email):
    payload = {
        'email' : email
    }
    
    return requests.post(config.url + "auth/passwordreset/request/v1", json = payload)
    

def password_reset(reset_code, new_password):
    payload = {
        'reset_code' : reset_code,
        'new_password' : new_password
    }
    
    return requests.post(config.url + "auth/passwordreset/reset/v1", json = payload)

