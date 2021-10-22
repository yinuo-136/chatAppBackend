import pytest
import requests
import json
from wrapper.auth_wrappers import auth_register
from wrapper.clear_wrapper import clear_http
from wrapper.admin_wrappers import admin_permission, admin_remove
from wrapper.user_wrappers import user_profile, list_users
from src import config

INPUT_ERROR = 400
ACCESS_ERROR = 403


def test_promote_permission():
    clear_http()

    r1 = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    r3 = auth_register("email1@gmail.com", "password123", "Nick", "Stath")
    token = r1.json()['token']
    token1 = r3.json()['token']
    
    # This should work as 'jayden' promotes 'Nick' to global owner
    r2 = admin_permission(token, 2, 1)
    assert r2.json() == {}
    
    # This should work as 'Nick' who is now a global owner, removes 'jayden'
    r4 = admin_remove(token1, 1)
    assert r4.json() == {}
    
def test_demote_permission():
    clear_http()

    r1 = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    r3 = auth_register("email1@gmail.com", "password123", "Nick", "Stath")
    token = r1.json()['token']
    token1 = r3.json()['token']
    
    # This should work as 'jayden' promotes 'Nick' to global owner
    r2 = admin_permission(token, 2, 1)
    assert r2.json() == {}
    
    # This should work as 'Nick' who is now a global owner, demotes 'jayden'
    r4 = admin_permission(token1, 1, 2)
    assert r4.json() == {}

#def test_channel_removal():
#def test_dm_removal():
#def test_messages_change():

def test_user_profile_remove():
    clear_http()

    r1 = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    token1 = r1.json()['token']
    auth_register("email1@gmail.com", "password123", "Nick", "Stath")

    # Jayden removes nick
    r2 = admin_remove(token1, 2)
    assert r2.json() == {}
    
    r3 = user_profile(token1, 2)
    
    # Nick's profile is still available
    assert r3.json() == {'user' : {
                        'u_id' : 2,
                        'email' : '',
                        'name_first' : 'Removed',
                        'name_last' : 'user',
                        'handle_str' : ''}
    }
    
    r4 = auth_register("email2@gmail.com", "password123", "New", "Person")
    assert r4.json()['auth_user_id'] == 3
     
def test_list_all_remove():
    clear_http()

    r1 = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    token1 = r1.json()['token']
    auth_register("email1@gmail.com", "password123", "Nick", "Stath")


    # Jayden removes nick
    r2 = admin_remove(token1, 2)
    assert r2.json() == {}
    
    r3 = list_users(token1)
    
    # Nick should not appear
    assert r3.json() == {'users' : [{
                        'u_id' : 1,
                        'email' : 'email@gmail.com',
                        'name_first' : 'Jayden',
                        'name_last' : 'Matthews',
                        'handle_str' : 'jaydenmatthews'}]
    }
    
def test_invalid_uid_remove():
    clear_http()

    r1 = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    
    token = r1.json()['token']
    
    r2 = admin_remove(token, 2)
    
    assert r2.status_code == INPUT_ERROR

def test_not_global_auth_remove():
    clear_http()
    
    auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    r1 = auth_register("email1@gmail.com", "password123", "Nick", "Stath")
    
    token = r1.json()['token']
    
    r2 = admin_remove(token, 1)
    
    assert r2.status_code == ACCESS_ERROR
    
    
def test_remove_only_global_permission():
    clear_http()

    r1 = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    
    token = r1.json()['token']
    
    r2 = admin_remove(token, 1)
    
    assert r2.status_code == INPUT_ERROR
    
    
def test_invalid_uid_permission():
    clear_http()

    r1 = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    
    token = r1.json()['token']
    
    r2 = admin_permission(token, 2, 1)
    
    assert r2.status_code == INPUT_ERROR
    
    
def test_not_global_owner_permission():
    clear_http()

    auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    r1 = auth_register("email1@gmail.com", "password123", "Nick", "Stath")
    
    token = r1.json()['token']
    
    r2 = admin_permission(token, 1, 2)
    
    assert r2.status_code == ACCESS_ERROR

    
def test_demote_only_global_permission():
    clear_http()

    r1 = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    
    token = r1.json()['token']
    
    r2 = admin_permission(token, 1, 2)
    
    assert r2.status_code == INPUT_ERROR
    
    
def test_invalid_permission_id():
    clear_http()

    r1 = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    auth_register("email1@gmail.com", "password123", "Nick", "Stath")
    
    token = r1.json()['token']
    
    r2 = admin_permission(token, 2, 3)
    
    assert r2.status_code == INPUT_ERROR

