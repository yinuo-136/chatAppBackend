'''
This file contains functions for registering a user and logging in a user.
'''
import hashlib
import re
from src.data_store import data_store
from src.error import InputError, AccessError
from src.config import url
from datetime import datetime, timezone
import typing

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

def auth_login_v1(email :str, password :str) ->typing.Dict[str, int]:
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


def auth_register_v1(email :str, password :str, name_first :str, name_last :str) ->typing.Dict[str, int]:
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
        
    
    #### INITIALISATION OF WORKSPACE STATS ####
    if len(store['registered_users'].keys()) == 0:
        workspace_type = typing.Dict[str, typing.Union[float, typing.List[typing.Dict[str, int]]]]
        workspace_stats : workspace_type = {}
        
        dt = datetime.now(timezone.utc)
        timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
        current_time = int(timestamp)  
        
        
        workspace_stats.update({'channels_exist' : [{'num_channels_exist' : 0, 'time_stamp' : current_time}]})
        workspace_stats.update({'dms_exist' : [{'num_dms_exist' : 0, 'time_stamp' : current_time}]})     
        workspace_stats.update({'messages_exist' : [{'num_messages_exist' : 0, 'time_stamp' : current_time}]}) 
        workspace_stats.update({'utilization_rate' : 0.0})
        
        store['workspace_stats'] = workspace_stats
        
    # Storing Details in Datastore
    new_id = len(store['user_details']) + 1    
    
    #### INITIAL USER STATS FOR EACH REGISTERING USER ####    
    user_stats = {}
    
    dt = datetime.now(timezone.utc)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    current_time = int(timestamp)  
    
    user_stats.update({'channels_joined' : [{'num_channels_joined' : 0, 'time_stamp' : current_time}]})
    user_stats.update({'dms_joined' : [{'num_dms_joined' : 0, 'time_stamp' : current_time}]})     
    user_stats.update({'messages_sent' : [{'num_messages_sent' : 0, 'time_stamp' : current_time}]})
    
    store['user_stats'].update({new_id : user_stats})  
    
    #img_url is default
    img_url = url + "static/default.jpg"

    #implementation of global permissions (1 for Owner, 2 for Member)
    if len(store['registered_users'].keys()) == 0:
        store['global_permissions'].update({new_id: 1})
    else:
        store['global_permissions'].update({new_id: 2})

    store['logged_in_users'].append(new_id)
    store['user_details'].update({new_id : (email, hashlib.sha256(password.encode()).hexdigest(), name_first, name_last, handle, img_url)})
    store['registered_users'].update({email: hashlib.sha256(password.encode()).hexdigest()})
    store['user_ids'].update({email: new_id})

    data_store.set(store)
    
    return {
        'auth_user_id': new_id,
    }
    
def auth_logout_v1(auth_user_id :int)->None:
    store = data_store.get()
    
    store['logged_in_users'].remove(auth_user_id)
    
def auth_store_session_id(u_id :int, session_id :int)->None:
    store = data_store.get()

    store['session_ids'].append((u_id, session_id))
   
def auth_invalidate_session(u_id :int, session_id :int)->None:

    store = data_store.get()

    for i, session in enumerate(store['session_ids']):
        if session[0] == u_id and session[1] == session_id:
            store['session_ids'].pop(i)
    
    data_store.set(store)

