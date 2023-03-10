from typing import Any
import requests
import json
import jwt
from requests.api import request
from src import config
from src.dm import dm_create_v1, dm_list_v1
from src.auth import auth_register_v1
from src.other import clear_v1

from wrapper.dm_wrappers import dm_create_wrapper, dm_list_wrapper, dm_remove_wrapper, dm_details_wrapper, dm_leave_wrapper, dm_messages_wrapper
from wrapper.auth_wrappers import auth_register
from wrapper.message_wrappers import senddm_message, react_message
from wrapper.clear_wrapper import clear_http

BASE_URL = config.url


# Status code constants
ACCESS_ERROR_CODE = 403
INPUT_ERROR_CODE = 400
SUCCESS = 200
# AccessError       code = 403
# InputError        code = 400

'''
    u_ids contains the user(s) that this DM is directed to, and will not include the creator. 
    
    The creator is the owner of the DM. name should be automatically generated based on the users that are in this DM. 
    
    The name should be an alphabetically-sorted, comma-and-space-separated list of user handles, e.g. 'ahandle1, bhandle2, chandle3'.
    
    '''






def test_dm_create__local():

    clear_v1()

    dct_1 = auth_register_v1("test1@gmail.com", "password", "Nicholas", "Stathakis")
    u_id_1 = dct_1['auth_user_id']

    dct_2 = auth_register_v1("test2@gmail.com", "password", "Zeddy", "Zarnacle")
    u_id_2 = dct_2['auth_user_id']

    dict_dm_id = dm_create_v1(u_id_1, [u_id_2])

    dm_id = dict_dm_id['dm_id']

    assert dm_id == 1


# r = auth_register("email@gmail.com", "password123", "Jayden", "Matthews")
    
#     resp = r.json()
    
#     assert type(resp['token']) is str
#     assert resp['auth_user_id'] == 1
    
#     clear_http()

#   InputError when: any u_id in u_ids does not refer to a valid user
def test_dm_create__fail__user_not_valid():

    #TODO: clear, 
    
    clear_http()

    # register a user, 
    
    r = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")
    # then call the function with user token and invalid_id

    data = r.json()

    my_user_token = data['token']
    invalid_user_id = [99]


    
    r = dm_create_wrapper(my_user_token, invalid_user_id)

    status_code = r.status_code

    assert status_code == INPUT_ERROR_CODE #input-error


#successful dm creation
def test_dm_create__success_basic():

    # TODO: clear, register two users, then post

    clear_http()


    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")
    r2 = auth_register("somerandom@gmail.com", "password123", "Jayden", "Matthews")

    # then call the function with user token and invalid_id

    data1 = r1.json()
    data2 = r2.json()


    my_user_token = data1['token']
    valid_other_id = data2['auth_user_id']


    
    r = dm_create_wrapper(my_user_token, [valid_other_id])
    dm_create_wrapper(my_user_token, [valid_other_id])

    status_code = r.status_code
    response_dict = json.loads(r.text)

    assert status_code == SUCCESS # aka 200 OK
    assert response_dict == { 'dm_id' : 1 } # should start at 1


def test_dm_create__success__double_dm():

    # TODO: clear, 
    
    clear_http()

     
    # register two users


    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")
    r2 = auth_register("somerandom@gmail.com", "password123", "Jayden", "Matthews")

    # then call the function with user token and invalid_id

    data1 = r1.json()
    data2 = r2.json()


    my_user_token = data1['token']
    valid_other_id = data2['auth_user_id']

    ############################ FIRST DM


    r = dm_create_wrapper(my_user_token, [valid_other_id])

    status_code = r.status_code
    response_dict = json.loads(r.text)

    assert status_code == SUCCESS # aka 200 OK
    assert response_dict == { 'dm_id' : 1 } # should start at 1


    ################################# SECOND DM

    r1 = auth_register("iamdifferent@gmail.com", "password123", "Kill", "Bill")
    # then call the function with user token and invalid_id

    data1 = r1.json()

    third_id = data1['auth_user_id']

    
    r = dm_create_wrapper(my_user_token, [valid_other_id, third_id])

    status_code = r.status_code
    response_dict = json.loads(r.text)

    assert status_code == SUCCESS # aka 200 OK
    assert response_dict == { 'dm_id' : 2 } # NEXT SHOULD BE 2 ID


#Note: cannot test that name of DM will be alphabetically sorted as that would break blackbox
##################################### END OF dm_create_v1 TESTS


#################################### START OF dm_list_v1 TESTS

def test_local__dm_list():

    clear_v1()

    dct_1 = auth_register_v1("test1@gmail.com", "password", "Nicholas", "Stathakis")
    u_id_1 = dct_1['auth_user_id']

    dct_2 = auth_register_v1("test2@gmail.com", "password", "Zeddy", "Zarnacle")
    u_id_2 = dct_2['auth_user_id']

    dict_dm_id = dm_create_v1(u_id_1, [u_id_2])

    dm_id = dict_dm_id['dm_id']

    assert dm_id == 1

    ret = dm_list_v1(u_id_2)
    dm = ret['dms']

    assert dm == [{'dm_id': 1, 'name': 'nicholasstathakis, zeddyzarnacle'}]


def test_dm_list__success__basic_owner():

    # TODO: Clear, 
    
    clear_http()


    # register two users, 
    
    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")
    r2 = auth_register("somerandom@gmail.com", "password123", "Zeddy", "Zarnacle")

    # then call the function with user token and invalid_id

    data1 = r1.json()
    data2 = r2.json()


    my_user_token = data1['token']
    valid_other_id = data2['auth_user_id']

    # and create a dm between the two

    dm_create_wrapper(my_user_token, [valid_other_id]) # note, we don't care about this, it is for later


    # NOW, test the list functionality

    
    r = dm_list_wrapper(my_user_token)

    status_code = r.status_code
    response_dict = json.loads(r.text)

    assert status_code == SUCCESS # aka 200 OK
    assert response_dict == { 'dms' : [{'dm_id': 1, 'name': 'nicholasstathakis, zeddyzarnacle'}] } # NEXT SHOULD BE 2 ID




def test_dm_list__success__basic_user():

    # TODO: Clear, 
    
    clear_http()


    # register two users, 
    
    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")
    r2 = auth_register("somerandom@gmail.com", "password123", "Zeddy", "Zarnacle")

    # then call the function with user token and invalid_id

    data1 = r1.json()
    data2 = r2.json()


    user_1_token = data1['token']

    user_2_token = data2['token']
    user_2_id = data2['auth_user_id']

    # and create a dm between the two

    dm_create_wrapper(user_1_token, [user_2_id]) # note, we don't care about this, it is for later


    # NOW, test the list functionality

    
    r = dm_list_wrapper(user_2_token)

    status_code = r.status_code
    response_dict = json.loads(r.text)

    assert status_code == SUCCESS # aka 200 OK
    assert response_dict == { 'dms' : [{'dm_id': 1, 'name': 'nicholasstathakis, zeddyzarnacle'}] } # NEXT SHOULD BE 2 ID



def test_dm_list__success__basic_user__additional_dms():

    # TODO: Clear, 
    
    clear_http()


    # register two users, 
    
    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")
    r2 = auth_register("somerandom@gmail.com", "password123", "Zeddy", "Zarnacle")
    r3 = auth_register("iamjelly@gmail.com", "password123", "Police", "Man")

    # then call the function with user token and invalid_id

    data1 = r1.json()
    data2 = r2.json()
    data3 = r3.json()


    user_1_token = data1['token']

    user_2_token = data2['token']
    user_2_id = data2['auth_user_id']

    user_3_id = data3['auth_user_id']

    # create two dms (1->2), (2->3)

    dm_create_wrapper(user_1_token, [user_2_id]) # note, we don't care about this, it is for later
    dm_create_wrapper(user_2_token, [user_3_id])

    # NOW, test the list functionality

    
    r = dm_list_wrapper(user_1_token)

    status_code = r.status_code
    response_dict = json.loads(r.text)

    assert status_code == SUCCESS # aka 200 OK
    assert response_dict == { 'dms' : [{'dm_id': 1, 'name': 'nicholasstathakis, zeddyzarnacle'}] } # NEXT SHOULD BE 2 ID


##################################### END OF dm_list_v1 TESTS


#################################### START OF dm_remove_v1 TESTS

'''
#Remove an existing DM, so all members are no longer in the DM. This can only be done by the original creator of the DM.
'''

def test_dm_remove__success_basic():

    #Clear

    clear_http()

    #Register two users

    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")
    r2 = auth_register("somerandom@gmail.com", "password123", "Jayden", "Matthews")

    # then call the function with user token and invalid_id

    data1 = r1.json()
    data2 = r2.json()


    user_1_token = data1['token']

    user_2_u_id = data2['auth_user_id']

    #Create dm

    r = dm_create_wrapper(user_1_token, [user_2_u_id])

    status_code = r.status_code
    assert status_code == SUCCESS


    response_message = json.loads(r.text)

    dm_id = response_message['dm_id']

    assert dm_id == 1

    # make owner remove dm

    # owner calls remove on their own dm
    r = dm_remove_wrapper(user_1_token, dm_id)

    status_code = r.status_code
    response_body = json.loads(r.text)


    assert response_body == {}
    assert status_code == SUCCESS





def test_dm_remove__error__dm_id_invalid():

    # TODO: Clear, 
    
    clear_http()
    
    # register one user,
    
    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")

    data1 = r1.json()

    my_user_token = data1['token']
    
    # try remove a invalid channel

    invalid_dm_id = 999

    print(f"Tok = {my_user_token}, invalid_id = {invalid_dm_id}")

    r = dm_remove_wrapper(my_user_token, invalid_dm_id)

    status_code = r.status_code

    assert status_code == INPUT_ERROR_CODE


def test_dm_remove__error__user_unauthorised():

    # TODO: Clear, 
    
    clear_http()


    # register TWO users

    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")
    r2 = auth_register("somerandom@gmail.com", "password123", "Jayden", "Matthews")

    # then call the function with user token and invalid_id

    data1 = r1.json()
    data2 = r2.json()


    user_1_token = data1['token']

    user_2_token = data2['token']
    user_2_u_id = data2['auth_user_id']

    
    r = dm_create_wrapper(user_1_token, [user_2_u_id])

    status_code = r.status_code
    assert status_code == SUCCESS


    response_message = json.loads(r.text)

    dm_id = response_message['dm_id']

    assert dm_id == 1

    # TODO: Get token of unauthorised u_id

    
    nr = dm_remove_wrapper(user_2_token, dm_id)

    new_status_code = nr.status_code

    assert new_status_code == ACCESS_ERROR_CODE



##################################### END OF dm_remove_v1 TESTS


#################################### START OF dm_details_v1 TESTS


def test_dm_details__success_basic():

    #Clear

    clear_http()

    #Register two users


    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")
    r2 = auth_register("somerandom@gmail.com", "password123", "Jayden", "Matthews")

    # then call the function with user token and invalid_id

    data1 = r1.json()
    data2 = r2.json()


    user_1_token = data1['token']

    user_2_token = data2['token']
    user_2_u_id = data2['auth_user_id']


    #Create a dm between the two users


    r = dm_create_wrapper(user_1_token, [user_2_u_id])

    status_code = r.status_code
    assert status_code == SUCCESS


    response_message = json.loads(r.text)

    dm_id = response_message['dm_id']

    assert dm_id == 1


    #Call dm_details_v1 and check output matches {name, members}


    r = dm_details_wrapper(user_2_token, dm_id)

    status_code = r.status_code
    response_body = json.loads(r.text)

    #r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")
    #r2 = auth_register("somerandom@gmail.com", "password123", "Jayden", "Matthews")

    assert response_body == { 'name' : "jaydenmatthews, nicholasstathakis",
                              'members' : [
                                  { 'u_id' : 1, 
                                    'email' : "test@gmail.com",
                                    'name_first' : "Nicholas",
                                    'name_last' : "Stathakis",
                                    'handle_str' : "nicholasstathakis",
                                    'profile_img_url' : config.url + "static/default.jpg"
                                },
                                  { 'u_id' : 2, 
                                    'email' : "somerandom@gmail.com",
                                    'name_first' : "Jayden",
                                    'name_last' : "Matthews",
                                    'handle_str' : "jaydenmatthews",
                                    'profile_img_url' : config.url + "static/default.jpg"
                                }                             
                              ] 
                            }

    assert status_code == SUCCESS # should be 200 OK as the user is apart of the dm and is therefore authorised



def test_dm_details__fail__dm_id_invalid():

    #Clear

    clear_http()

    #Register one user


    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")

    data1 = r1.json()


    user_1_token = data1['token']
    invalid_dm_id = 999

    r = dm_details_wrapper(user_1_token, invalid_dm_id)

    status_code = r.status_code

    assert status_code == INPUT_ERROR_CODE # InputError as per interace spec.


def test_dm_details__fail__user_not_member__valid_dm_id():

    #clear

    clear_http()

    #register three users

    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")
    r2 = auth_register("somerandom@gmail.com", "password123", "Jayden", "Matthews")
    r3 = auth_register("iamslime@gmail.com", "password123", "Miles", "Wick")

    # then call the function with user token and invalid_id

    data1 = r1.json()
    data2 = r2.json()
    data3 = r3.json()


    user_1_token = data1['token']

    user_2_u_id = data2['auth_user_id']

    user_3_token = data3['token']


    #create chat between TWO only


    r = dm_create_wrapper(user_1_token, [user_2_u_id])

    status_code = r.status_code
    assert status_code == SUCCESS


    response_message = json.loads(r.text)

    dm_id = response_message['dm_id']

    assert dm_id == 1

    # call dm_details_v1 with third members NOT in the dm with the correct dm id


    r = dm_details_wrapper(user_3_token, dm_id)

    status_code = r.status_code

    assert status_code == ACCESS_ERROR_CODE



##################################### END OF dm_details_v1 TESTS


#################################### START OF dm_leave_v1 TESTS


def test_dm_leave__success__basic_member():

    #TODO: Clear

    clear_http()

    # Add two users

    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")
    r2 = auth_register("somerandom@gmail.com", "password123", "Jayden", "Matthews")

    data1 = r1.json()
    data2 = r2.json()

    user_1_token = data1['token']

    user_2_token = data2['token']
    user_2_u_id = data2['auth_user_id']


    # Create a dm between them

    r = dm_create_wrapper(user_1_token, [user_2_u_id])

    response_message = json.loads(r.text)
    dm_id = response_message['dm_id']
    assert dm_id == 1

    # Make one user leave
    
    
    r = dm_leave_wrapper(user_2_token, dm_id)



    status_code = r.status_code
    response_body = json.loads(r.text)



    assert status_code == SUCCESS
    assert response_body == {}
    # Check channel details to see if they are removed



def test_dm_leave__success__basic_owner():

    #TODO: Clear

    clear_http()

    # Add two users

    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")
    r2 = auth_register("somerandom@gmail.com", "password123", "Jayden", "Matthews")

    data1 = r1.json()
    data2 = r2.json()

    user_1_token = data1['token']

    user_2_u_id = data2['auth_user_id']


    # Create a dm between them

    r = dm_create_wrapper(user_1_token, [user_2_u_id])

    response_message = json.loads(r.text)
    dm_id = response_message['dm_id']
    assert dm_id == 1

    # Make one user leave
    
    
    r = dm_leave_wrapper(user_1_token, dm_id)



    status_code = r.status_code
    response_body = json.loads(r.text)



    assert status_code == SUCCESS
    assert response_body == {}
    # Check channel details to see if they are removed




def test_dm_leave__fail__dm_id_invalid():

    # Clear

    clear_http()

    # Register a user

    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")    
    data1 = r1.json()
    
    user_1_token = data1['token']
    invalid_dm_id = 99

    # Leave with invalid ID

    r = dm_leave_wrapper(user_1_token, invalid_dm_id)

    status_code = r.status_code

    assert status_code == INPUT_ERROR_CODE



def test_dm_leave__fail__user_not_member():

    #Clear

    clear_http()

    #Register three users

    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")
    r2 = auth_register("somerandom@gmail.com", "password123", "Jayden", "Matthews")
    r3 = auth_register("iamslime@gmail.com", "password123", "Miles", "Wick")

    data1 = r1.json()
    data2 = r2.json()
    data3 = r3.json()


    user_1_token = data1['token']
    user_2_u_id = data2['auth_user_id']
    user_3_token = data3['token']

    # Create dm between two

    r = dm_create_wrapper(user_1_token, [user_2_u_id])

    response_body = json.loads(r.text)
    dm_id = response_body['dm_id']

    # Third user try leave that dm

    r = dm_leave_wrapper(user_3_token, dm_id)

    status_code = r.status_code

    assert status_code == ACCESS_ERROR_CODE

    # Assert status code is ACCESS ERROR


##################################### END OF dm_leave_v1 TESTS


#################################### START OF dm_messages_v1 TESTS


def test_dm_messages__success__basic_more_than_fifty_messages():

    #TODO: Clear

    clear_http()

    # Register two users


    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")
    r2 = auth_register("somerandom@gmail.com", "password123", "Jayden", "Matthews")

    data1 = r1.json()
    data2 = r2.json()

    user_1_token = data1['token']

    user_2_u_id = data2['auth_user_id']


    # Make a dm

    r = dm_create_wrapper(user_1_token, [user_2_u_id])

    response_message = json.loads(r.text)
    dm_id = response_message['dm_id']
    assert dm_id == 1


    # send one message

    for x in range(51):
        x
        senddm_message(user_1_token, dm_id, 'this is spam')
    

    # Request messages for this dm


    r = dm_messages_wrapper(user_1_token, dm_id, 0)

    status_code = r.status_code
    response = json.loads(r.text)

    assert status_code == SUCCESS

    messages = response['messages']
    start = int(response['start'])
    end = int(response['end'])

    assert len(messages) == 50
    assert start == 0
    assert end == 50




def test_dm_messages__success__basic_one_message():

    #TODO: Clear

    clear_http()

    # Register two users


    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")
    r2 = auth_register("somerandom@gmail.com", "password123", "Jayden", "Matthews")

    data1 = r1.json()
    data2 = r2.json()

    user_1_token = data1['token']

    user_2_u_id = data2['auth_user_id']


    # Make a dm

    r = dm_create_wrapper(user_1_token, [user_2_u_id])

    response_message = json.loads(r.text)
    dm_id = response_message['dm_id']
    assert dm_id == 1


    # send one message

    m_id = senddm_message(user_1_token, dm_id, 'hello1')

    react_message(user_1_token, m_id, 1)
    # Request messages for this dm


    r = dm_messages_wrapper(user_1_token, dm_id, 0)

    status_code = r.status_code
    response = json.loads(r.text)

    assert status_code == SUCCESS

    messages = response['messages']
    content = messages[0]['message']
    start = int(response['start'])
    end = int(response['end'])

    assert len(messages) == 1
    assert content == 'hello1'
    assert start == 0
    assert end == -1




def test_dm_messages__fail__dm_id_invalid():

    #Clear

    clear_http()


    # Register one user

    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")    
    data1 = r1.json()
    
    user_1_token = data1['token']
    invalid_dm_id = 99

    # try to get messages for invalid dm id

    r = dm_messages_wrapper(user_1_token, invalid_dm_id, 0)

    status_code = r.status_code

    assert status_code == INPUT_ERROR_CODE


def test_dm_messages__fail__start_greater_than_total():

    # Clear

    clear_http()


    # Add two users

    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")
    r2 = auth_register("somerandom@gmail.com", "password123", "Jayden", "Matthews")

    data1 = r1.json()
    data2 = r2.json()

    user_1_token = data1['token']

    user_2_token = data2['token']
    user_2_u_id = data2['auth_user_id']


    # Create a dm between them

    r = dm_create_wrapper(user_1_token, [user_2_u_id])

    response_message = json.loads(r.text)
    dm_id = response_message['dm_id']
    assert dm_id == 1

    # Try call dm_messages_v1 with no messages sent

    r = dm_messages_wrapper(user_2_token, dm_id, 1)

    status_code = r.status_code

    assert status_code == INPUT_ERROR_CODE



def test_dm_messages__fail__user_not_member():

    # Clear

    clear_http()

    # register 3 users

    r1 = auth_register("test@gmail.com", "password123", "Nicholas", "Stathakis")
    r2 = auth_register("somerandom@gmail.com", "password123", "Jayden", "Matthews")
    r3 = auth_register("iamslime@gmail.com", "password123", "Miles", "Wick")

    data1 = r1.json()
    data2 = r2.json()
    data3 = r3.json()


    user_1_token = data1['token']
    user_2_u_id = data2['auth_user_id']
    user_3_token = data3['token']

    # Create dm between two

    r = dm_create_wrapper(user_1_token, [user_2_u_id])

    response_body = json.loads(r.text)
    dm_id = response_body['dm_id']

    # Make third person request messages

    r = dm_messages_wrapper(user_3_token, dm_id, 0)

    status_code = r.status_code

    # Raise Access Error

    assert status_code == ACCESS_ERROR_CODE
