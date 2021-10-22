import pytest
import jwt
from src import config
from wrapper.auth_wrappers import auth_register, auth_logout
from wrapper.clear_wrapper import clear_http
# These tests will use auth_logout which runs the token_checker

def test_invalid_user_id():
    clear_http()
    
    r1 = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    
    token = r1.json()['token']
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    session_id = payload.get('session_id')
    
    false_token = jwt.encode({'user_id' : 3, 'session_id' : session_id}, config.SECRET, algorithm="HS256")
    
    r2 = auth_logout(false_token)
    
    assert r2.status_code == 403

def test_invalid_session_id():
    clear_http()
    
    r1 = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    
    token = r1.json()['token']
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
    
    false_token = jwt.encode({'user_id' : user_id, 'session_id' : 'thisisnotarealsessionid'}, config.SECRET, algorithm="HS256")
    
    r2 = auth_logout(false_token)
    
    assert r2.status_code == 403

