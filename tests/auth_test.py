import pytest

from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1
from src.data_store import *


def test_basic_auth_single():

    clear_v1()

    assert auth_register_v1("email@gmail.com", "password", "First", "Last") == { 'auth_user_id' : 1 }


def test_basic_auth_multiple():

    clear_v1()

    assert auth_register_v1("email@gmail.com", "password", "Jayden", "Matthews") == { 'auth_user_id' : 1 }
    assert auth_register_v1("email@yahoo.com", "password", "Nick", "Stathakis") == { 'auth_user_id' : 2 }
    assert auth_register_v1("email@outlook.com", "password", "Sample", "Name") == { 'auth_user_id' : 3 }


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


def test_basic_failed_login__email():

    clear_v1()

    auth_register_v1("test@gmail.com", "password", "First", "Last")

    with pytest.raises(InputError):
        auth_login_v1("not_correct@yahoo.com", "password")


def test_basic_failed_login__password():

    clear_v1()

    auth_register_v1("test@gmail.com", "password", "First", "Last")

    with pytest.raises(InputError):
        auth_login_v1("test@gmail.com", "not_correct")


def test_basic_failed_register__invalid_email():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("invalid_email", "password", "Nick", "Stathakis")


def test_basic_failed_register__duplicate_email():

    clear_v1()

    auth_register_v1("test@gmail.com", "password", "Nick", "Stathakis")

    with pytest.raises(AccessError):
        auth_register_v1("test@gmail.com", "another_password", "Jayden", "Matthews")


def test_basic_failed_register__small_password():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "four", "Nick", "Stathakis")


def test_success_register__valid_first():

    clear_v1()

    auth_register_v1("test@gmail.com", "password", "MyNameIsVeryLongButStillValid123", "Stathakis")


def test_failed_register__invalid_first__empty():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "password", "", "Stathakis")


def test_failed_register__invalid_first__more_than_fifty():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "password", "ThisStringIsMoreThanFiftyCharactersXXXXXXXXXXXXXXXX", "Stathakis")


def test_failed_register__invalid_first__invalid_characters():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "password", "I$Am_Invalid+-", "Stathakis")


def test_success_register__valid_last():

    clear_v1()

    auth_register_v1("test@gmail.com", "password", "FirstName", "MyLastNameIsVeryLongButStillValid123")


def test_failed_register__invalid_last__empty():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "password", "FirstName", "")


def test_failed_register__invalid_last__more_than_fifty():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "password", "FirstName", "ThisStringIsMoreThanFiftyCharactersXXXXXXXXXXXXXXXX")


def test_failed_register__invalid_last__invalid_characters():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "password", "FirstName", "I$Am_Invalid+-")

def test_basic_handle():
    auth_register_v1("email@gmail.com", "password" , "jayden" , "matthews")
    
    store = data_store.get()
    
    user = store['user_details'].get(1)
    assert user[4] == "jaydenmatthews"
    
    clear_v1()

def test_duplicate_handle():
    auth_register_v1("email@gmail.com", "password" , "jayden" , "matthews")
    auth_register_v1("email2@gmail.com", "password2" , "jayden" , "matthews")
    auth_register_v1("email3@gmail.com", "password3" , "jayden" , "matthews")
    auth_register_v1("email4@gmail.com", "password4" , "jayden" , "matthews")
    
    store = data_store.get()
    
    user = store['user_details'].get(1)
    assert user[4] == "jaydenmatthews"  
    user = store['user_details'].get(2)
    assert user[4] == "jaydenmatthews0"
    user = store['user_details'].get(3)
    assert user[4] == "jaydenmatthews1"
    user = store['user_details'].get(4)
    assert user[4] == "jaydenmatthews2"
    
    clear_v1()
    
def test_long_name():
    auth_register_v1("email@gmail.com", "password" , "thisisalongstring" , "lastnamelong")
    
    store = data_store.get()
    
    user = store['user_details'].get(1)
    assert user[4] == "thisisalongstringlas"
    
    clear_v1()
