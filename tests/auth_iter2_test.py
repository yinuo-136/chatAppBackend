import pytest
import requests
import uuid
import json
from wrapper.auth_wrappers import auth_register, auth_login, auth_logout
from wrapper.clear_wrapper import clear_http
from src import config


ACCESS_ERROR = 403
INPUT_ERROR = 400

def test_basic_auth_register():
    clear_http()
    
    r = auth_register("email@gmail.com", "password123", "Jaydeeennnn", "Mattttheewwss")
    
    resp = r.json()
    
    assert type(resp['token']) is str
    assert resp['auth_user_id'] == 1

    
def test_basic_auth_login_logout():
    clear_http()
        
    auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    r = auth_login("email@gmail.com", "password123")
    
    resp = r.json()
    
    assert type(resp['token']) is str
    assert resp['auth_user_id'] == 1
    
    
    r1 = auth_logout(resp['token'])
     
    assert r1.json() == {}

# Inccorect Email - InputError
def test_incorrect_email_login():
    clear_http()
    auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    r = auth_login("wrong@gmail.com", "password123")
    
    assert r.status_code == INPUT_ERROR
    

# Inccorect Password - Input Error 
def test_incorrect_password_login():
    clear_http()

    auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    r = auth_login("email@gmail.com", "wrongpassword")
    
    assert r.status_code == INPUT_ERROR
    
# Non Valid Email
def test_invalid_email_register(): 
    clear_http()
    r = auth_register("invalid.com", "password123", "Jayden", "Matthews")
    
    assert r.status_code == INPUT_ERROR
    
    
# Email Already in Use
def test_duplicate_email_register(): 
    clear_http()
    
    auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    r = auth_register("email@gmail.com", "password123", "Nick", "Stath")
    assert r.status_code == INPUT_ERROR
    
    
# Password len < 6
def test_password_len_register(): 
    clear_http()
    
    r = auth_register("email@gmail.com", "pswrd", "Jayden", "Matthews")
    
    assert r.status_code == INPUT_ERROR
    
# Name > 50 or < 1
def test_long_first_name_register(): 
    clear_http()
    
    r = auth_register("email@gmail.com", "password123", "j" * 51, "Matthews")
    
    assert r.status_code == INPUT_ERROR
    

def test_short_first_name_register(): 
    clear_http()
    r = auth_register("email@gmail.com", "password123", "", "Matthews")
    
    assert r.status_code == INPUT_ERROR

    
# Last Name > 50 or < 1
def test_long_last_name_register(): 
    clear_http()
    
    r = auth_register("email@gmail.com", "password123", "Jayden", "m" * 51)
    
    assert r.status_code == INPUT_ERROR

def test_short_last_name_register(): 
    clear_http()
    
    r = auth_register("email@gmail.com", "password123", "Jayden", "")
    
    assert r.status_code == INPUT_ERROR
 
def test_cool():
    clear_http()
    
    auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    auth_register("email1@gmail.com", "password123", "Nick", "Stath")
    
    assert True
    
    
