'''
This file contains functions for registering a user and logging in a user.
'''
import hashlib
import re
from src.data_store import data_store
from src.error import InputError, AccessError

def check_user_details(password, name_first, name_last):
    '''
    Checks the validity/length of passwords and users first/last name

    Arguments:
        <password> (<string>)    - <password of registered user>
        <name_first> (<string>)  - <first name of user>
        <name_last> (<string>)   - <last name of user>

    Exceptions:
        InputError  - Occurs when password, name_first, or name_last are not of
        adequate length.

    Return Value:
        Returns <None>
    '''

    #error checking for password
    if len(password) < 6:
        raise InputError("Password is less than 6 characters!")

    #error checking for name
    if len(name_first) > 50 or len(name_first) < 1:
        raise InputError("First Name must be between 1 and 50 characters!")

    if len(name_last) > 50 or len(name_last) < 1:
        raise InputError("Last Name must be between 1 and 50 characters!")

def auth_login_v1(email, password):
    '''
    <Logs a user into Streams and appends them to logged_in_users member in
    data_store, includes relevant error checking>

    Arguments:
        <email> (<string>)    - <email of the user>
        <password> (<string>)    - <password of the user>

    Exceptions:
        InputError  - Occurs when email doesnt exist or password incorrect.

    Return Value:
        Returns <auth_user_id>
    '''

    store = data_store.get()
    # if email not in store['registered_users'].keys() raise error
    if email not in store['registered_users'].keys():
        raise InputError("Email does not exist!")

    # if email in store['registered_users'].keys(), but password not matching, raise error
    if hashlib.sha256(password.encode()).hexdigest() != store['registered_users'].get(email):
        raise InputError("Incorrect password!")

    store['logged_in_users'].append(store['user_ids'].get(email))

    return {
        'auth_user_id': store['user_ids'].get(email),
    }


def auth_register_v1(email, password, name_first, name_last):
    '''
    <Registers a new user with the Streams platform>

    Arguments:
        <email> (<string>)       - <email of the user>
        <password> (<string>)    - <password of the user>
        <name_first> (<string>)  - <first name of user>
        <name_last> (<string>)   - <last name of user>
        ...

    Exceptions:
        InputError  - Occurs when email is not valid format,
        AccessError - Occurs when duplicate email is provided

    Return Value:
        Returns <auth_user_id>
    '''
    store = data_store.get()
    #implement error for email
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'

    if re.fullmatch(regex, email) is None:
        raise InputError("Non-valid email format!")

    #implement error checking for duplicate
    if email in store['registered_users'].keys():
        raise InputError("A user with that email already exists")


    #error checking for password and user name
    check_user_details(password, name_first, name_last)

    handle_first = "".join(x for x in name_first if x.isalnum())
    handle_last = "".join(x for x in name_last if x.isalnum())

    #HANDLE implementation
    handle = handle_first + handle_last
    handle = handle.lower()

    if len(handle) > 20:
        handle = handle[0:20]

    handle_matches = 0
    for i in store['user_details'].keys():
        user = store['user_details'][i]
        temp_handle = re.sub(r'[0-9]+', '', user[4])
        print(temp_handle)
        if temp_handle == handle:
            handle_matches += 1

    if handle_matches > 0:
        handle = handle + str(handle_matches - 1)


    # Storing Details in Datastore
    new_id = len(store['user_details']) + 1

    #implementation of global permissions (1 for Owner, 2 for Member)
    if len(store['registered_users'].keys()) == 0:
        store['global_permissions'].update({new_id: 1})
    else:
        store['global_permissions'].update({new_id: 2})

    store['logged_in_users'].append(new_id)
    store['user_details'].update({new_id : (email, hashlib.sha256(password.encode()).hexdigest(), name_first, name_last, handle)})
    store['registered_users'].update({email: hashlib.sha256(password.encode()).hexdigest()})
    store['user_ids'].update({email: new_id})

    data_store.set(store)
    
    return {
        'auth_user_id': new_id,
    }
    
def auth_logout_v1(auth_user_id):
    store = data_store.get()
    
    store['logged_in_users'].remove(auth_user_id)
    
def auth_store_session_id(session_id):
    store = data_store.get()

    store['session_ids'].append(session_id)
   
def auth_invalidate_session(session_id):
    store = data_store.get()

    store['session_ids'].remove(session_id)

