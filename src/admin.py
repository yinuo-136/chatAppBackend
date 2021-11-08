from src.data_store import data_store
from src.error import InputError, AccessError

def is_only_global_owner():
    store = data_store.get()
    
    num_global_owners = 0
    
    for permission in store['global_permissions'].values():
        if permission == 1:
            num_global_owners += 1
    
    if num_global_owners == 1:
        return True
    else:
        return False   
     
def admin_user_remove(auth_user_id, u_id):
    store = data_store.get()
    
    if u_id not in store['user_details'].keys():
        raise InputError("u_id does not exist!")
    
    if store['global_permissions'].get(auth_user_id) != 1:
        raise AccessError("You are not authorised to remove users!")
    
    if store['global_permissions'].get(u_id) == 1 and is_only_global_owner():
        raise InputError("Cannot remove the only global owner!")
   
    ''' Given a user by their u_id, remove them from the Streams. This means they should
     be removed from all channels/DMs, and will not be included in the list of users returned 
     by users/all. 
     - Streams owners can remove other Streams owners (including the original 
     first owner). 
     - Once users are removed, the contents of the messages they sent will be replaced by 'Removed user'. 
     - Their profile must still be retrievable with user/profile, however name_first should be 'Removed' and name_last should be 'user'. 
     - The user's email and handle should be reusable.'''
        
    # Remove user from channels
    for channel in store['channels'].values():
        if u_id in channel[2]:
            channel[2].remove(u_id)
        if u_id in channel[3]:
            channel[3].remove(u_id)
        
    # Remove user from dms 
    for dm in store['dms'].values():
        if u_id == dm['owner_id']:
            dm['owner_id'] = None
        if u_id in dm['u_ids']:
            dm['u_ids'].remove(u_id)
        
    # Change users messages
    for message in store['messages'].values():
        if message[0] == u_id:
            message[1] = 'Removed user'
    

    # Change users name_first and name_last
    user = store['user_details'].get(u_id)
    u_email = user[0]
    
    # Remove user from data_store entries
    store['registered_users'].pop(u_email)
    store['user_ids'].pop(u_email)
    # list(filter(lambda x: x != u_id, store['logged_in_users'])) ????
    
    # Change users name_first and name_last, remove handle and email
    store['user_details'].update({u_id : ("", user[1], 'Removed', 'user', "", user[5])})
    
    data_store.set(store)
    
    
def admin_permission_change(auth_user_id, u_id, permission_id):
    store = data_store.get()

    if u_id not in store['user_details'].keys():
        raise InputError("u_id does not exist!")
    
    if store['global_permissions'].get(auth_user_id) != 1:
        raise AccessError("You are not authorised to change user permissions!")
    
    if store['global_permissions'].get(u_id) == 1 and is_only_global_owner() and permission_id == 2:
        raise InputError("Cannot demote the only global owner!")
        
    if permission_id != 1 and permission_id != 2:
        raise InputError("Permission id must be either 1 or 2")
        
    store['global_permissions'].update({u_id : permission_id})
    
    data_store.set(store)
    

