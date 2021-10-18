from src.error import InputError
from src.error import AccessError
from src.data_store import data_store

# TODO(nick): this function. It is currently a stub.
def dm_create_v1(owner_u_id, u_ids):

    '''
    u_ids contains the user(s) that this DM is directed to, and will not include the creator. 
    
    The creator is the owner of the DM. name should be automatically generated based on the users that are in this DM. 
    
    The name should be an alphabetically-sorted, comma-and-space-separated list of user handles, e.g. 'ahandle1, bhandle2, chandle3'.
    
    '''

    store = data_store.get()

    all_u_ids = store['user_details']
    
    #InputError when: any u_id in u_ids does not refer to a valid user
    # ASSUMPTION: owner id is not present within this...
    for u_id in u_ids:
        if u_id not in all_u_ids.keys():
            raise InputError("One of the given u_id's does not refer to a valid user") 


    dict_dms = store['dms']

    dm_id = len(dict_dms) + 1 # start dm length from 1 onwards
    owner_id = owner_u_id
    members = u_ids
    messages = {}

    # "dm_id" : {'owner_id' : 1, 'u_ids': [2,3,4], 'messages' : {},}

    dict_dms.update({dm_id : {
        'owner_id' : owner_id,
        'u_ids' : members,
        'messages' : messages
    }})

    # dummy code for `dm_id` return
    return { 'dm_id' : dm_id }