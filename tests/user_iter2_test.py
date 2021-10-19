import pytest
import requests
import json
from src import config
from wrapper.auth_wrappers import auth_register, auth_login, auth_logout
from wrapper.user_wrappers import user_profile, set_email, set_handle, set_name
from wrapper.clear_wrapper import clear_http

def test_basic_user_profile():
    
    clear_http()

    auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    
    r = user_profile(1)
    
    assert r.json() == {'user' : {
                        'u_id' : 1,
                        'email' : 'email@gmail.com',
                        'name_first' : 'Jayden',
                        'name_last' : 'Matthews',
                        'handle_str' : 'jaydenmatthews'}
    }
    
    clear_http()
    
def test_basic_set_name():
    
    auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    
    r = set_name(1, 'newfirst', 'newlast')
    assert r.json() == {}
    
    r1 = user_profile(1)
    assert r1.json() == {'user' : {
                        'u_id' : 1,
                        'email' : 'email@gmail.com',
                        'name_first' : 'newfirst',
                        'name_last' : 'newlast',
                        'handle_str' : 'jaydenmatthews'}
    }
    
    clear_http()

def test_basic_set_email():

    auth_register("email@gmail.com", "password123", "Jayden", "Matthews")    
    
    r = set_email(1, 'new@email.com')
    assert r.json() == {}
    
    r1 = user_profile(1)
    assert r1.json() == {'user' : {
                        'u_id' : 1,
                        'email' : 'new@email.com',
                        'name_first' : 'Jayden',
                        'name_last' : 'Matthews',
                        'handle_str' : 'jaydenmatthews'}
    }
    
    clear_http()
        
def test_basic_set_handle():

    auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    
    r = set_handle(1, 'newhandlestr')
    assert r.json() == {}
    
    r1 = user_profile(1)
    assert r1.json() == {'user' : {
                        'u_id' : 1,
                        'email' : 'email@gmail.com',
                        'name_first' : 'Jayden',
                        'name_last' : 'Matthews',
                        'handle_str' : 'newhandlestr'}
    }
    
    clear_http()
