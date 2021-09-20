import pytest

from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1


def test_basic_auth_single():
    clear_v1()
    assert auth_register_v1("email@gmail.com", "password", "First", "Last") == { 'auth_user_id' : 1 }


def test_basic_auth_multiple():
    clear_v1()
    assert auth_register_v1("email@gmail.com", "password", "Jayden", "Matthews") == { 'auth_user_id' : 1 }
    assert auth_register_v1("email@yahoo.com", "password", "Nick", "Stathakis") == { 'auth_user_id' : 2 }
    assert auth_register_v1("email@outlook.com", "password", "Sample", "Name") == { 'auth_user_id' : 3 }