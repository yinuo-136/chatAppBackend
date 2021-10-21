from src.error import InputError
from src.error import AccessError
from src.data_store import data_store
from src.user import user_details
from itertools import islice


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
    messages = []

    #print(f"Dm Name: \'{dm_name}\'")

    # STRUCTURE:
    #       "dm_id" : {'name' : 'a, b, c', owner_id' : 1, 'u_ids': [2,3,4], 'messages' : {},}

    dict_dms.update({dm_id : {
        'name' : dm_name,
        'owner_id' : owner_id,
        'u_ids' : members,
        'messages' : messages,
    }})

    data_store.set(store)


    # dummy code for `dm_id` return
    return { 'dm_id' : dm_id }


def dm_list_v1(member_id):

    '''
    Returns { dms } => List of dictionaries, where each dictionary contains types { dm_id, name } 

    Returns the list of DMs that the user is a member of.
    '''

    store = data_store.get()

    all_u_ids = store['user_details']
    
    #InputError when: any u_id in u_ids does not refer to a valid user
    # ASSUMPTION: we raise an ACCESS ERROR
    if member_id not in all_u_ids.keys():
        raise AccessError("User ID does not exist") 


    all_dm_dict = store['dms']

    dms = []

    for curr_dm_id in all_dm_dict.keys():
        #print(f"Currently at dm id: {curr_dm_id}")

        dm_obj = all_dm_dict[curr_dm_id]
        #print(dm_obj)

        owner_id = dm_obj['owner_id']
        u_ids = dm_obj['u_ids']
        
        is_apart_of_dm = False

        # if user is owner, add this to the return dms dict
        if member_id is owner_id:
            is_apart_of_dm = True

        # if user is a member of u_ids, add this to return dms dict
        if member_id in u_ids:
            is_apart_of_dm = True


        # append to list which stores all dm_id and name of dm's user is apart of
        if is_apart_of_dm:
            to_add = {'dm_id' : curr_dm_id, 'name' : dm_obj['name']}
            dms.append(to_add)


    return { 'dms' : dms }



# Remove an existing DM, so all members are no longer in the DM. This can only be done by the original creator of the DM.
def dm_remove_v1(u_id, dm_id):

    '''
    Parameters:     { token, dm_id }
    Return Type:    {}
    '''


    # firstly check dm_id is a valid dm

    store = data_store.get()

    all_dm_dict = store['dms']
        
    dm_exists = (dm_id in all_dm_dict.keys())
    
        
    # if we are given a number larger than number of dms OR smaller than 1 (minimum valid dm num)
    if (dm_exists == False):
        raise InputError("dm_id does not refer to a valid DM")


    # next, check authorised user is original creator

    specific_dm = all_dm_dict[dm_id]

    owner_id = specific_dm['owner_id']

    if (owner_id != u_id):
        raise AccessError("dm_id is valid and the authorised user is not the original DM creator")



    # proceed to goods

    #print(all_dm_dict)
    all_dm_dict.pop(dm_id) # remove this entry from the dm dict
    #print(all_dm_dict)

    
    return {}



def dm_details_v1(auth_u_id, dm_id):

    '''
    Given a DM with ID dm_id that the authorised user is a member of, provide basic details about the DM.
    
    Parameters:     { token, dm_id }
    Return Type:    { name, members }
    '''

    #InputError when: dm_id does not refer to a valid DM

    store = data_store.get()

    all_dm_dict = store['dms']
        
    dm_exists = (dm_id in all_dm_dict.keys())
    
    if (dm_exists == False):
        raise InputError("dm_id does not refer to a valid DM")

    #AccessError when: dm_id is valid and the authorised user is not a member of the DM


    specific_dm = all_dm_dict[dm_id]

    all_members = specific_dm['u_ids']
    
    owner_id = specific_dm['owner_id'] #our owner id
    all_members.append(owner_id)

    #"dm_id" : {'name' : 'a, b, c', owner_id' : 1, 'u_ids': [2,3,4], 'messages' : {},}


    user_is_member = (auth_u_id in all_members)


    if (not user_is_member):
        raise AccessError("dm_id is valid and the authorised user is not a member of the DM")

    # continue on, yahoo! its-a-me, mario.


    name = specific_dm['name']
    members = []

    for u_id in all_members:
        members.append(user_details(u_id)) #method taken from `user.py` which gets our `user` data structure

    return { 'name' : name,
             'members' : members }






def dm_leave_v1(auth_u_id, dm_id):

    #Input error when dm_id is INVALID

    store = data_store.get()

    all_dm_dict = store['dms']
        
    dm_exists = (dm_id in all_dm_dict.keys())
    
    if (dm_exists == False):
        raise InputError("dm_id does not refer to a valid DM")


    #AccessError when dmid is valid and authorised user is NOT member of DM


    specific_dm = all_dm_dict[dm_id]

    all_members = specific_dm['u_ids']
    
    owner_id = specific_dm['owner_id'] #our owner id
    all_members.append(owner_id)

    user_is_member = (auth_u_id in all_members)


    if (not user_is_member):
        raise AccessError("dm_id is valid and the authorised user is not a member of the DM")

    # we are gravy

    is_owner = (auth_u_id is owner_id)

    

    # STRUCTURE:
    #       "dm_id" : {'name' : 'a, b, c', owner_id' : 1, 'u_ids': [2,3,4], 'messages' : {},}

    # dict_dms.update({dm_id : {
    #     'name' : dm_name,
    #     'owner_id' : owner_id,
    #     'u_ids' : members,
    #     'messages' : messages,
    # }})

    dm_name = specific_dm['name']
    owner_id = specific_dm['owner_id']
    u_ids = specific_dm['u_ids']
    messages = specific_dm['messages']

    if (is_owner):
        # remove them from the 'owner_id'
        owner_id = None
    else:
        # remove them from 'u_ids'
        u_ids.remove(auth_u_id)

    store['dms'].update({ dm_id: {
        'name' : dm_name,
        'owner_id' : owner_id,
        'u_ids' : u_ids,
        'messages' : messages,
    }})

    data_store.set(store)
    
    return {}



def dm_messages_v1(auth_u_id, dm_id, start):

    '''
    Given a DM with ID dm_id that the authorised user is a member of, return up to 50 messages between index "start" and "start + 50". 
    
    Message with index 0 is the most recent message in the DM. 
    
    This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the DM, 
    returns -1 in "end" to indicate there are no more messages to load after this return.
    
    '''

    #InputError when any of: dm_id does not refer to a valid DM
    
    store = data_store.get()

    all_dm_dict = store['dms']
        
    dm_exists = (dm_id in all_dm_dict.keys())
    
    if (dm_exists == False):
        raise InputError("dm_id does not refer to a valid DM")
        
    #Input Error when: start is greater than the total number of messages in the channel
    

    specific_dm = all_dm_dict[dm_id]

    dm_messages = specific_dm['messages']
    num_msgs = len(dm_messages)

    # index 0 is the first message, therefore start = 0 will have len 1. thus there are no msgs applicable if start > len(msgs) - 1
    if (start > num_msgs - 1):
        raise InputError("start is greater than the total number of messages in the channel")


    
    # AccessError when: dm_id is valid and the authorised user is not a member of the DM


    all_members = specific_dm['u_ids']
    
    owner_id = specific_dm['owner_id'] #our owner id
    all_members.append(owner_id)

    user_is_member = (auth_u_id in all_members)


    if (not user_is_member):
        raise AccessError("dm_id is valid and the authorised user is not a member of the DM")


    # lets get to the implementation

    store_messages = store['messages'] # a dict {}
    # and we have dm_messages = []


    # reverse so most recent are at index 0 (since they are appended instead of insert 0)
    #set end as an invalid number first
    m_list = list(islice(reversed(dm_messages), start, start + 50))

    end = -1

    if num_msgs > start + 50:
        end = start + 50


    messages = []
    for m_id in m_list:

        
        message_id = m_id
        u_id = store_messages[m_id][0]
        message = store_messages[m_id][1]
        time_created = store_messages[m_id][2]


        messages.append({
                'message_id': message_id,
                'u_id': u_id,
                'message': message,
                'time_created': time_created
            })    



    return { 'messages' : messages,
             'start' : start,
             'end' : end, }