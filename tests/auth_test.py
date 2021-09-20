import pytest

from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1


def test_basic_auth_single():
    clear_v1()
    assert auth_register_v1("email@gmail.com", "password", "First", "Last") == { 'auth_user_id' : 1 }


def test_basic_auth_multiple():
    clear_v1()
    assert auth_register_v1("email@gmail.com", "password", "Jayden", "Matthews") == { 'auth_user_id' : 1 }
    assert auth_register_v1("email@yahoo.com", "password", "Nick", "Stathakis") == { 'auth_user_id' : 2 }
    assert auth_register_v1("email@outlook.com", "password", "Sample", "Name") == { 'auth_user_id' : 3 }

def test_basic_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("invalid_email", "password", "Nick", "Stathakis")

def test_basic_no_duplicates():
    clear_v1()
    auth_register_v1("test@gmail.com", "password", "First", "Last")
    with pytest.raises(AccessError):
        auth_register_v1("test@gmail.com", "password", "First", "Last")

def test_full_workflow_correct():
    clear_v1()
    register_details = auth_register_v1("test@gmail.com", "password", "First", "Last")
    auth_user_id_reg = register_details["auth_user_id"]

    login_details = auth_login_v1("test@gmail.com", "password")
    auth_user_id_log = login_details["auth_user_id"]

    assert auth_user_id_log == auth_user_id_reg

