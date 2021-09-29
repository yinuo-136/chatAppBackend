import pytest

from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1
from src.data_store import *


@pytest.fixture
def clear_and_register_single_user():

    clear_v1()

    result = auth_register_v1("test@gmail.com", "password", "First", "Last")

    return result

@pytest.fixture
def register_single_user():

    result = auth_register_v1("test@gmail.com", "password", "First", "Last")

    return result





def test_basic_auth_single(clear_and_register_single_user):

    assert clear_and_register_single_user == { 'auth_user_id' : 1 }


def test_basic_auth_multiple():

    clear_v1()

    assert auth_register_v1("email@gmail.com", "password", "Jayden", "Matthews") == { 'auth_user_id' : 1 }
    assert auth_register_v1("email@yahoo.com", "password", "Nick", "Stathakis") == { 'auth_user_id' : 2 }
    assert auth_register_v1("email@outlook.com", "password", "Sample", "Name") == { 'auth_user_id' : 3 }


def test_basic_no_duplicates(clear_and_register_single_user):

    clear_and_register_single_user

    with pytest.raises(AccessError):
        auth_register_v1("test@gmail.com", "password", "First", "Last")


def test_full_workflow_correct():

    clear_v1()

    register_details = auth_register_v1("test@gmail.com", "password", "First", "Last")
    auth_user_id_reg = register_details["auth_user_id"]

    login_details = auth_login_v1("test@gmail.com", "password")
    auth_user_id_log = login_details["auth_user_id"]

    assert auth_user_id_log == auth_user_id_reg


def test_basic_failed_login__email(clear_and_register_single_user):

    clear_and_register_single_user

    with pytest.raises(InputError):
        auth_login_v1("not_correct@yahoo.com", "password")


def test_basic_failed_login__password(clear_and_register_single_user):

    clear_and_register_single_user

    with pytest.raises(InputError):
        auth_login_v1("test@gmail.com", "not_correct")


def test_basic_failed_register__invalid_email():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("invalid_email", "password", "Nick", "Stathakis")


def test_basic_failed_register__duplicate_email(clear_and_register_single_user):

    clear_and_register_single_user

    with pytest.raises(AccessError):
        auth_register_v1("test@gmail.com", "another_password", "Jayden", "Matthews")


def test_basic_failed_register__small_password():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "four", "Nick", "Stathakis")


def test_success_register__valid_first():

    clear_v1()

    auth_register_v1("test@gmail.com", "password", "a" * 36, "Stathakis")


def test_failed_register__invalid_first__empty():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "password", "", "Stathakis")


def test_failed_register__invalid_first__more_than_fifty():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "password", "a" * 51, "Stathakis")


def test_failed_register__invalid_first__invalid_characters():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "password", "I$Am_Invalid+-", "Stathakis")


def test_success_register__valid_last():

    clear_v1()

    auth_register_v1("test@gmail.com", "password", "FirstName", "a" * 36)


def test_failed_register__invalid_last__empty():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "password", "FirstName", "")


def test_failed_register__invalid_last__more_than_fifty():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "password", "FirstName", "a" * 51)


def test_failed_register__invalid_last__invalid_characters():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "password", "FirstName", "I$Am_Invalid+-")


def test_basic_handle():

    clear_v1()

    auth_register_v1("test@gmail.com", "password" , "Jayden" , "Matthews")
    
    store = data_store.get()
    
    user = store['user_details'].get(1)
    assert user[4] == "jaydenmatthews"
    
    


def test_duplicate_handle():

    clear_v1()

    auth_register_v1("email1@gmail.com", "password1" , "Jayden" , "Matthews")
    auth_register_v1("email2@gmail.com", "password2" , "Jayden" , "Matthews")
    auth_register_v1("email3@gmail.com", "password3" , "Jayden" , "Matthews")
    auth_register_v1("email4@gmail.com", "password4" , "Jayden" , "Matthews")
    
    store = data_store.get()
    
    user = store['user_details'].get(1)
    assert user[4] == "jaydenmatthews"  

    user = store['user_details'].get(2)
    assert user[4] == "jaydenmatthews0"

    user = store['user_details'].get(3)
    assert user[4] == "jaydenmatthews1"
    
    user = store['user_details'].get(4)
    assert user[4] == "jaydenmatthews2"
    
    


def test_long_name():

    clear_v1()

    auth_register_v1("email@gmail.com", "password" , "a" * 19 , "b" * 10)
    
    store = data_store.get()
    
    user = store['user_details'].get(1)
    assert user[4] == "a" * 19 + "b"
    
    

   
def test_basic_global_permissions():

    clear_v1()

    auth_register_v1("email1@gmail.com", "password1" , "jayden" , "matthews")
    auth_register_v1("email2@gmail.com", "password2" , "nick" , "stath")
    auth_register_v1("email3@gmail.com", "password3" , "other" , "guy")
    
    store = data_store.get()
    
    user_id1 = store['user_ids'].get("email1@gmail.com")
    user_id2 = store['user_ids'].get("email2@gmail.com")    
    user_id3 = store['user_ids'].get("email3@gmail.com")    
    
    assert store['global_permissions'].get(user_id1) == 1
    assert store['global_permissions'].get(user_id2) == 2
    assert store['global_permissions'].get(user_id3) == 2
    
    
