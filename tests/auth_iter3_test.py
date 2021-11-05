import requests
from src import config
from src.data_store import data_store
from src.other import clear_v1
from wrapper.clear_wrapper import clear_http
from wrapper.auth_wrappers import auth_register, auth_login, auth_logout
from wrapper.password_wrappers import password_request, password_reset
from src.password import password_request_v1, password_reset_v1
from src.auth import auth_register_v1, auth_login_v1

''' These are tests for the request password change functionality.'''

INPUT_ERROR = 400
ACCESS_ERROR = 403

def test_basic_request_password_change():
    clear_http()
    
    r1 = auth_register("jaymatt2232@gmail.com", "password", "Jayden", "Matthews")
    auth_register("different@gmail.com", "yipson123", "Nick", "Statho")
    
    #multiple sessions
    r2 = auth_login("jaymatt2232@gmail.com", "password")
    token2 = r2.json()['token']
    
    r3 = auth_login("jaymatt2232@gmail.com", "password")   
    token3 = r3.json()['token']
    
    r4 = password_request("jaymatt2232@gmail.com")
    assert r4.json() == {}
    
    # These should fail as the users sessions/tokens have been invalidated
    r5 = auth_logout(token2)
    assert r5.status_code == ACCESS_ERROR
    
    r6 = auth_logout(token3)
    assert r6.status_code == ACCESS_ERROR


def test_too_short_password_reset():
    clear_http()
    
    r = password_reset("RESETCODE", "short")
    
    assert r.status_code == INPUT_ERROR
    
    
def test_invalid_code_password_reset():
    clear_http()
    
    #populating with real codes
    password_request("jaymatt2232@gmail.com")
    password_request("jaymatt2232@gmail.com")
    
    r = password_reset("FAKECODE42", "password123")
    
    assert r.status_code == INPUT_ERROR

def test_whitebox_password_reset():
    clear_v1()
    
    auth_register_v1("jaymatt2232@gmail.com", "password", "Jayden", "Matthews")
    
    password_request_v1("jaymatt2232@gmail.com") 
    
    
    reset_code = data_store.get()['unique_codes'][0][1]
    assert data_store.get()['unique_codes'][0][0] == 1
    
    password_reset_v1("newpassword", reset_code)
    

    # Should work as password has been reset    
    assert auth_login_v1("jaymatt2232@gmail.com", "newpassword") == {
        'auth_user_id': 1,
    }
    
    
   
    
    
