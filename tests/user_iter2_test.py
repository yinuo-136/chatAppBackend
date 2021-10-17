import pytest
import requests
import json
from src import config
from tests.user_wrappers import user_profile, set_email, set_handle, set_name

def test_basic_user_profile():
    
    r = user_profile(1)
    
    assert r.json() == {'user' : {
                        'u_id' : 1,
                        'email' : 'email@gmail.com',
                        'name_first' : 'Jayden',
                        'name_last' : 'Matthews',
                        'handle_str' : 'jaydenmatthews'}
    }
    
def test_basic_set_name():
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

def test_basic_set_email():
    r = set_email(1, 'new@email.com')
    assert r.json() == {}
    
    r1 = user_profile(1)
    assert r1.json() == {'user' : {
                        'u_id' : 1,
                        'email' : 'new@email.com',
                        'name_first' : 'newfirst',
                        'name_last' : 'newlast',
                        'handle_str' : 'jaydenmatthews'}
    }
    
def test_basic_set_handle():
    r = set_handle(1, 'newhandlestr')
    assert r.json() == {}
    
    r1 = user_profile(1)
    assert r1.json() == {'user' : {
                        'u_id' : 1,
                        'email' : 'new@email.com',
                        'name_first' : 'newfirst',
                        'name_last' : 'newlast',
                        'handle_str' : 'newhandlestr'}
    }
    
