import pytest

from src.other import clear_v1
from src.auth import auth_register_v1


################# START OF PYTEST FIXTURES #################

# uses method clear_v1 and registers a user with the details:
#       email: test@gmail.com
#       password: password
#       first_name: First
#       last_name: Last
@pytest.fixture
def clear_and_register_single_user():

    clear_v1()

    result = auth_register_v1("test@gmail.com", "password", "First", "Last")

    return result



# registers four users with emails "test1@gmail.com", "test2@gmail.com", "test3@gmail.com" and "test4@gmail.com"
@pytest.fixture
def register_four_users():

    auth_register_v1("test1@gmail.com", "password", "First", "Last")
    auth_register_v1("test2@gmail.com", "password", "First", "Last")
    auth_register_v1("test3@gmail.com", "password", "First", "Last")
    auth_register_v1("test4@gmail.com", "password", "First", "Last")





################# START OF BLACKBOX TESTS #################

# blackbox test which will test that data is successfully cleared in a duplicate registration
def test_clear__basic_register_single(clear_and_register_single_user):

    # register user once
    clear_and_register_single_user

    # clear and register same user -- notice no duplicate errors being thrown!
    clear_and_register_single_user



# test clearing with multiple users registered
def test_clear__register_multiple(register_four_users):

    register_four_users

    clear_v1()

    register_four_users