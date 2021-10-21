import pytest
import requests
import json
from src import config
from wrapper.auth_wrappers import auth_register, auth_login, auth_logout
from wrapper.user_wrappers import user_profile, set_email, set_handle, set_name, list_users
from wrapper.clear_wrapper import clear_http
from src.data_store import data_store

ACCESS_ERROR = 403
INPUT_ERROR = 400

def test_basic_user_profile():
    clear_http()
    
    r = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    token = r.json()['token']
    
    r1 = user_profile(token, 1)
    
    assert r1.json() == {'user' : {
                        'u_id' : 1,
                        'email' : 'email@gmail.com',
                        'name_first' : 'Jayden',
                        'name_last' : 'Matthews',
                        'handle_str' : 'jaydenmatthews'}
    }
    
def test_basic_set_name():
    clear_http()
    r1 = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    token = r1.json()['token']

    r2 = set_name(token, 'newfirst', 'newlast')
    assert r2.json() == {}
    
    r3 = user_profile(token, 1)
    assert r3.json() == {'user' : {
                        'u_id' : 1,
                        'email' : 'email@gmail.com',
                        'name_first' : 'newfirst',
                        'name_last' : 'newlast',
                        'handle_str' : 'jaydenmatthews'}
    }
    


def test_basic_set_email():
    clear_http()
    
    r = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    token = r.json()['token'] 
    
    r1 = set_email(token, 'new@email.com')
    assert r1.json() == {}
    
    r2 = user_profile(token, 1)
    assert r2.json() == {'user' : {
                        'u_id' : 1,
                        'email' : 'new@email.com',
                        'name_first' : 'Jayden',
                        'name_last' : 'Matthews',
                        'handle_str' : 'jaydenmatthews'}
    }
  
        
def test_basic_set_handle():
    clear_http()
    
    r = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    token = r.json()['token']
    
    r1 = set_handle(token, 'newhandlestr')
    assert r1.json() == {}
    
    r2 = user_profile(token, 1)
    assert r2.json() == {'user' : {
                        'u_id' : 1,
                        'email' : 'email@gmail.com',
                        'name_first' : 'Jayden',
                        'name_last' : 'Matthews',
                        'handle_str' : 'newhandlestr'}
    }
      

# user/all
# Write a test for multiple users, repeat handles 
def test_basic_user_all():
    clear_http()
    
    auth_register("email1@gmail.com", "password1", "Jayden", "Matthews")
    r = auth_register("email2@gmail.com", "password2", "Jayden", "Matthews")
    token = r.json()['token']
    
    r1 = list_users(token)
    
    assert r1.json() == {'users' : [{
                        'u_id' : 1,
                        'email' : 'email1@gmail.com',
                        'name_first' : 'Jayden',
                        'name_last' : 'Matthews',
                        'handle_str' : 'jaydenmatthews'}, {
                        'u_id' : 2,
                        'email' : 'email2@gmail.com',
                        'name_first' : 'Jayden',
                        'name_last' : 'Matthews',
                        'handle_str' : 'jaydenmatthews0'}]
    }    
# user/profile
# Non-existent user_id passed
def test_invalid_u_id_profile():
    clear_http()
    
    r = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    token = r.json()['token']
    
    r1 = user_profile(token, 2)
    assert r1.status_code == INPUT_ERROR

def test_long_first_set_name():
    clear_http()
        
    r = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    token = r.json()['token']
        
    r1 = set_name(token, 'j' * 51, 'newlast')
    assert r1.status_code == INPUT_ERROR
    
def test_long_last_set_name():
    clear_http()
        
    r = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    token = r.json()['token']
        
    r1 = set_name(token, 'newfirst', 'j' * 51)
    assert r1.status_code == INPUT_ERROR

def test_invalid_format_set_email():
    clear_http()
    
    r = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    token = r.json()['token'] 
    
    r1 = set_email(token, 'invalid.com')
    assert r1.status_code == INPUT_ERROR

def test_duplicate_set_email():
    clear_http()
    
    auth_register("email2@gmail.com", "password123", "Nick", "Stath")
    r = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    token = r.json()['token'] 
    
    r1 = set_email(token, 'email2@gmail.com')
    assert r1.status_code == INPUT_ERROR

def test_long_set_handle():
    clear_http()
    
    r = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    token = r.json()['token']
    
    r1 = set_handle(token, 'h' * 21)
    assert r1.status_code == INPUT_ERROR
    
def test_short_set_handle():
    clear_http()
    
    r = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    token = r.json()['token']
    
    r1 = set_handle(token, 'hh')
    assert r1.status_code == INPUT_ERROR
    
def test_non_alnum_set_handle():
    clear_http()
    
    r = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    token = r.json()['token']
    
    r1 = set_handle(token, '1n#va*l&@id!')
    assert r1.status_code == INPUT_ERROR
    
def test_duplicate_set_handle():
    clear_http()
    
    auth_register("email2@gmail.com", "password123", "Nick", "Stath")
    r = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    token = r.json()['token']
    
    r1 = set_handle(token, 'nickstath')
    assert r1.status_code == INPUT_ERROR

