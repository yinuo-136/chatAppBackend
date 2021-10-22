import re
from src.data_store import data_store
from src.error import InputError, AccessError


def user_details(u_id):
    store = data_store.get()
    
    if u_id not in store['user_details'].keys():
        raise InputError("The u_id provided doesn't exist")
    
    user = store['user_details'].get(u_id)
    
    return {
        'u_id' : u_id,
        'email' : user[0],
        'name_first' : user[2],
        'name_last' : user[3],
        'handle_str' : user[4]
    }

def list_all_users():
    store = data_store.get()
    users = []
    
    for u_id, user in store['user_details'].items():
        if user[0] == "" and user[4] == "" and user[2] == 'Removed' and user[3] == 'user':
            continue
        else:
            users.append({
                'u_id' : u_id,
                'email' : user[0],
                'name_first' : user[2],
                'name_last' : user[3],
                'handle_str' : user[4]
            })
    
    return users

def user_set_name(u_id, name_first, name_last):
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError("First name must be between 1 and 50 characters")
    elif len(name_last) < 1 or len(name_last) > 50:
        raise InputError("Last name must be between 1 and 50 characters")
        
    store = data_store.get()
    
    user = list(store['user_details'].get(u_id))
    user[2] = name_first
    user[3] = name_last
    
    user = tuple(user)
    store['user_details'].update({u_id: user})

def user_set_email(u_id, email):
    #implement error for email
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'

    if re.fullmatch(regex, email) is None:
        raise InputError("Non-valid email format!")
    
    store = data_store.get()
    
    #implement error checking for duplicate
    if email in store['registered_users'].keys():
        raise InputError("A user with that email already exists")

    user = list(store['user_details'].get(u_id))
    user[0] = email
    
    user = tuple(user)
    store['user_details'].update({u_id: user})

def user_set_handle(u_id, handle_str):
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError("Handle length must be between 3 to 20 characters")
    elif handle_str.isalnum() == False:
        raise InputError("Handle contains non-alphanumeric characters")
     
    store = data_store.get()
    
    for user_id, usr in store['user_details'].items():
        if user_id != u_id and usr[4] == handle_str:
            raise InputError("Handle is taken by another user")
    
    user = list(store['user_details'].get(u_id))
    user[4] = handle_str
    
    user = tuple(user)
    
    store['user_details'].update({u_id: user})
