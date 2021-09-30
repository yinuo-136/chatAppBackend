import pytest

from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1

# import pytest fixture
from tests.clear_test import clear_and_register_single_user


################# START OF BLACKBOX TESTS #################

# test that a single user can successfully register
def test_basic_successful_register__single(clear_and_register_single_user):

    clear_and_register_single_user


# test multiple users can register successfully
def test_basic_successful_register__multiple():

    clear_v1()

    # register 3 different users, should all work successfully (no exceptions raised)
    auth_register_v1("test1@gmail.com", "password", "Person", "Lastname")
    auth_register_v1("test2@gmail.com", "password", "Person", "Lastname")
    auth_register_v1("test3@gmail.com", "password", "Person", "Lastname")


# test that if a duplicate email is detected then it fails
def test_basic_failed_register__duplicates(clear_and_register_single_user):

    # registers a user with email = "test@gmail.com"
    clear_and_register_single_user

    # registers another user with the SAME email, causing an AccessError
    with pytest.raises(AccessError):
        auth_register_v1("test@gmail.com", "password", "First", "Last")


# tests the workflow of registering and login, making sure the data returned is consistent
def test_full_register_and_login_successful(clear_and_register_single_user):

    # register user1 and store the user id returned
    u_id_register = clear_and_register_single_user

    # login to user1 and store user id returned
    u_id_login = auth_login_v1("test@gmail.com", "password")

    # make sure these two id's are the same
    assert u_id_register == u_id_login


# test that an incorrect email throws an InputError during LOGIN
def test_failed_login__email_invalid(clear_and_register_single_user):

    clear_and_register_single_user

    with pytest.raises(InputError):
        auth_login_v1("not_correct@yahoo.com", "password")


# test that an incorrect password throws an InputError during LOGIN
def test_failed_login__password_invalid(clear_and_register_single_user):

    clear_and_register_single_user

    with pytest.raises(InputError):
        auth_login_v1("test@gmail.com", "not_correct")


# test that an invalid email fails during REGISTRATION
def test_failed_register__email_invalid():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("invalid_email", "password", "Nick", "Stathakis")


# test that a duplicate email during registration FAILS and throws an AccessError
def test_failed_register__duplicate_email(clear_and_register_single_user):

    # register a user with the email = "test@gmail.com"
    clear_and_register_single_user

    with pytest.raises(AccessError):
        auth_register_v1("test@gmail.com", "another_password", "Jayden", "Matthews")


# test that an InputError is thrown when a password is invalid -- too small
def test_failed_register__small_password():

    clear_v1()

    # an invalid password of 4 characters (must be greater than 6)
    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "four", "Nick", "Stathakis")


# test that a user can successfully register with a 50 character First name (the limit)
def test_successful_register__long_first():

    clear_v1()

    auth_register_v1("test@gmail.com", "password", "a" * 50, "Stathakis")


# test that an empty first name throws an InputError exception
def test_failed_register__empty_first():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "password", "", "Stathakis")


# test that a first name GREATER than 50 characters throws an InputError
def test_failed_register__first_more_than_fifty():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "password", "a" * 51, "Stathakis")

# test that the maximum characters of last name (50) is valid
def test_success_register__last_long():

    clear_v1()

    auth_register_v1("test@gmail.com", "password", "FirstName", "a" * 50)


# test that if the last name is empty then a InputError is thrown
def test_failed_register__last_empty():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "password", "FirstName", "")


# test that if the last name exceeds the maximum of 50 characters, an InputError is thrown
def test_failed_register__last_more_than_fifty():

    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1("test@gmail.com", "password", "FirstName", "a" * 51)


############### End of Blackbox testing -- see whitebox/auth_white_test.py for whitebox tests