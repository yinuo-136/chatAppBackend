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

    # stores all user handles, will be sorted alphabetically and joined later on
    all_user_handles = []

    all_user_details = store['user_details']

    for u_id in u_ids:

        curr_handle = all_user_details[u_id][4]

        #print(f'>> {curr_handle}')

        all_user_handles.append(curr_handle)

    owner_handle = all_user_details[owner_u_id][4]
    #print(f'>>> {owner_handle}')

    # append owner to this list of all handles
    all_user_handles.append(owner_handle)

    #print(f"All Handles: {all_user_handles}")

    # sort the handles alphabetically
    all_user_handles = sorted(all_user_handles)

    #print(f"Sorted: {all_user_handles}")


    

    # all of our fields for the dict
    dm_id = len(dict_dms) + 1 # start dm length from 1 onwards
    dm_name = ', '.join(all_user_handles)
    owner_id = owner_u_id
    members = u_ids
    messages = {}

    #print(f"Dm Name: \'{dm_name}\'")

    # STRUCTURE:
    #       "dm_id" : {'name' : 'a, b, c', owner_id' : 1, 'u_ids': [2,3,4], 'messages' : {},}

    dict_dms.update({dm_id : {
        'name' : dm_name,
        'owner_id' : owner_id,
        'u_ids' : members,
        'messages' : messages,
    }})


    # dummy code for `dm_id` return
    return { 'dm_id' : dm_id }


def dm_list_v1(member_id):

    '''
    Returns the list of DMs that the user is a member of.
    '''

    store = data_store.get()

    all_u_ids = store['user_details']
    
    #InputError when: any u_id in u_ids does not refer to a valid user
    # ASSUMPTION: we raise an ACCESS ERROR
    if member_id not in all_u_ids.keys():
        raise AccessError("User ID does not exist") 


    all_dm_dict = store['dms']

    dms = {}

    for dm_obj in all_dm_dict.keys():
        print(dm_obj)

    '''
    returns { dms } => List of dictionaries, where each dictionary contains types { dm_id, name } 
    '''

