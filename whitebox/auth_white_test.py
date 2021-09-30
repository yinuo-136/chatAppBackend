from src.auth import auth_register_v1
from src.other import clear_v1
from src.data_store import *

# import pytest fixture
from tests.clear_test import clear_and_register_single_user


################# START OF WHITEBOX TESTS #################

# basic whitebox test for valid handle
def test_basic_valid_handle(clear_and_register_single_user):

    clear_and_register_single_user
    
    store = data_store.get()
    
    user = store['user_details'].get(1)
    assert user[4] == "firstlast"
    
    
# basic whitebox test for duplicate handles having extra characters appended properly
def test_basic_handle__duplicate():

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
    
    

# basic whitebox test for checking a long name is concatenated and capped correctly at 20 characters
def test_valid_handle__long_name():

    clear_v1()

    auth_register_v1("email@gmail.com", "password" , "a" * 19 , "b" * 10)
    
    store = data_store.get()
    
    user = store['user_details'].get(1)
    assert user[4] == "a" * 19 + "b"
    
    

# basic whitebox test for global permissions being stored properly   
def test_basic_global_permissions():

    clear_v1()

    auth_register_v1("email1@gmail.com", "password1" , "Jayden" , "Matthews")
    auth_register_v1("email2@gmail.com", "password2" , "Nick" , "Stath")
    auth_register_v1("email3@gmail.com", "password3" , "Other" , "Guy")
    
    store = data_store.get()
    
    user_id1 = store['user_ids'].get("email1@gmail.com")
    user_id2 = store['user_ids'].get("email2@gmail.com")    
    user_id3 = store['user_ids'].get("email3@gmail.com")    
    
    assert store['global_permissions'].get(user_id1) == 1
    assert store['global_permissions'].get(user_id2) == 2
    assert store['global_permissions'].get(user_id3) == 2
    

#Basic test for non-alnum first/last name, and resulting handle   
def test_non_alphanumeric_handle_basic():
    clear_v1()
    auth_register_v1("email1@gmail.com", "password1" , "J@yd!n" , "M@++hew$")
    
    store = data_store.get()
    
    u_id = store['user_ids'].get("email1@gmail.com")
    user = store['user_details'].get(u_id)
    
    assert user[4] == "jydnmhew"
    
    
    
    
    
