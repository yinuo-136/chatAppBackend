from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
import re

def auth_login_v1(email, password):
    store = data_store.get()
    # if email not in store['registered_users'].keys() raise error
    if email not in store['registered_users'].keys():
        print("Email doesnt exist!")
        raise InputError()
    
    # if email in store['registered_users'].keys(), but password not matching, raise error
    elif password != store['registered_users'].get(email):
        print("Wrong Password")
        raise InputError()
    
    else:
        store['logged_in_users'].append(store['user_ids'].get(email))
    return {
        'auth_user_id': store['user_ids'].get(email),
    }

def auth_register_v1(email, password, name_first, name_last):
    store = data_store.get()
    #implement HANDLE
    
    
    
    #implement error for email 
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    
    if re.fullmatch(regex, email) == None:
        raise InputError()
    
    #implement error checking for duplicate
    if email in store['registered_users'].keys():
        raise AccessError()
    
    #error checking for password
    
    if len(password) < 6:
        raise InputError()
    
    #error checking for name
    if len(name_first) > 50 or len(name_first) < 1:
        raise InputError()
        
    if len(name_last) > 50 or len(name_last) < 1:
        raise InputError()
   
    #error checking for non-alnum in name     
    name_regex = r'^[A-Za-z0-9]*$'   
    
    if re.fullmatch(name_regex, name_first) == None:
        raise InputError()
    elif re.fullmatch(name_regex, name_last) == None:
        raise InputError()
    
    
    # Storing Details in Datastore
    new_id = len(store['registered_users']) + 1
     
    store['user_details'].update({new_id : (email, password, name_first, name_last)})
    store['registered_users'].update({email: password})
    store['user_ids'].update({email: new_id})
    print(store['user_details'])
    print(store['registered_users'])
    
    return {
        'auth_user_id': new_id,
    }
