from src.error import InputError
from src.error import AccessError
from src.data_store import data_store
from itertools import islice


def channel_invite_v1(auth_user_id, channel_id, u_id):
    '''
    <Invites a user with ID u_id to join a channel with ID channel_id.>
    <Once invited, the user is added to the channel immediately.>

    Arguments:
        <auth_user_id> (integer)    - authorised user id
        <channel_id> (integer)    - channel_id
        <u_id> (integer)     - id of user to be added
    
    Exceptions:
        InputError  - Occurs when 1. auth_user_id is not valid
                                  2. channel_id is not valid
                                  3. u_id is not valid
                                  4. u_id is already a member of the channel
        AccessError - Occurs when 1. auth_user_id is not valid
                                  2. the authorised user is not a member of the channel

    Return Value:
        Returns an empty dictionary 
    '''
    store = data_store.get()

    #check channel_id is valid
    if channel_id not in store['channels'].keys():
        raise InputError("channel ID is not valid")

    #check u_id is valid
    if u_id not in store['user_details'].keys():
        raise InputError("The u_id is not valid")

    #check u_id is already member of channel_details_v1
    channel = store['channels'].get(channel_id)
    if (u_id in channel[2]) or (u_id in channel[3]):
        raise InputError("The u_id is is already a member of the channel")

    #check whether auth_user_id is a member of the channel
    if auth_user_id not in channel[3]:
        raise AccessError("Auth_User is not a member of the channel")

    
    members = channel[3]
    members.append(u_id)
    
    c_name = channel[0]
    c_public = channel[1]
    c_owners = channel[2]
    c_members = members
    c_messages = channel[4]
    
    store['channels'].update({channel_id : (c_name, c_public, c_owners, c_members, c_messages)})
    
    return {}

def channel_details_v1(auth_user_id, channel_id):
    '''
    <Provides basic channel details about the relevant channel>

    Arguments:
        <auth_user_id> (integer)    - auth_user_id
        <channel_id> (integer)    -channel_id
    
    Exceptions:
        InputError  - Occurs when 1. channel_id does not refer to a valid channel
        AccessError - Occurs when 1. if auth user id is not valid
                                  2. the authorised user is not a member of the channel

                                   
    Return Value:
        returns a dictionary containing 'name', 'is_public', 'owner_members', 'all_members'.
    '''
    store = data_store.get()

    #check if channel_id refers to a valid channel
    if channel_id not in store['channels'].keys():
        raise InputError("channel_id does not refer to a valid channel")

    #check if auth_user_id has access to channel
    channel = store['channels'].get(channel_id)
    if auth_user_id not in channel[3]:
        raise AccessError("auth_user_id does not have access to channel")

    #provide basic details about the channel
    user_details = store['user_details']
    owners = []
    members = []

    for u_id in channel[2]:
        user = user_details.get(u_id)
        owners.append({
            'u_id': u_id,
            'email': user[0],
            'name_first': user[2],
            'name_last': user[3],
            'handle_str': user[4],
        })

    for u_id in channel[3]:
        user = user_details.get(u_id)
        members.append({
            'u_id': u_id,
            'email': user[0],
            'name_first': user[2],
            'name_last': user[3],
            'handle_str': user[4],
        })

    return {
        'name': channel[0],
        'is_public': channel[1],
        'owner_members': owners,
        'all_members': members
    }


def channel_messages_v1(auth_user_id, channel_id, start):
    '''
    <return 50 messages from the start point in a channel>

    Arguments:
        <auth_user_id> (integer)    - user id
        <channel_id> (integer)    -channel_id
        <start> (integer)     - the start point where the messages should be cllected from
   ''' 
    store = data_store.get()
    
    #implement the channel id validity check
    c_dict = store['channels']
    if channel_id not in c_dict.keys():
        raise InputError(description="channel_id does not refer to a valid channel")

    #implement the user membership check
    c_info = c_dict[channel_id]
    c_members = c_info[3]
    if auth_user_id not in c_members:
        raise AccessError(description="the authorised user is not a member of the channel")

    #implement the start number check
    c_messages = c_info[4]

    if start < 0 :
        raise InputError(description="start number needs to be greater or equal to zero")

    if len(c_messages) < start:
        raise InputError(description="start is greater than the total number of messages in the channel")
    
    #set end as an invalid number first
    m_list = list(islice(reversed(c_messages), start, start + 50))
    end = -100
    if len(c_messages) > 50 + start:
        end = 50 + start
    else:       
        end = -1

    m_dict = store['messages']
    m_info = []
    for m_id in m_list:
        message_id = m_id
        u_id = m_dict[m_id][0]
        message = m_dict[m_id][1]
        shared_message = m_dict[m_id][4]
        time_created = m_dict[m_id][2]

        #get the reacts list of the message
        react_dict = m_dict[m_id][5]
        reacts = []       
        for react_id in react_dict.keys():
            is_this_user_reacted = False
            u_ids = react_dict[react_id]
            if auth_user_id in u_ids:
                is_this_user_reacted = True
            reacts.append({'react_id': react_id,
                        'u_ids': u_ids,
                        'is_this_user_reacted': is_this_user_reacted})
            

        m_info.append({
                'message_id': message_id,
                'u_id': u_id,
                'message': message + shared_message,
                'time_created': time_created,
                'reacts': reacts})    
    
    return {
        'messages': m_info,
        'start': start,
        'end': end
    }

def channel_join_v1(auth_user_id, channel_id):
    '''
    <allows authorised user to join the channel>

    Arguments:
        <auth_user_id> (integer)    - user id
        <channel_id> (integer)    - channel_id
    
    Exceptions:
        InputError  - Occurs when 1. channel_id does not refer to a valid channel
                                  2. auth_user is already a member
                                  3. start is greater than the total number of messages in the channel
        AccessError - Occurs when 1. the auth user id you entered does not exist
                                  2. the channel is private and the auth_user is not a global owner

                                  
    Return Value:
        empty dictionary
    '''

    store = data_store.get()

    channel = store['channels'].get(channel_id)

    #error checking for invalid channel_id
    if channel_id not in store['channels'].keys():
        raise InputError("channel_id is not valid")


    #error checking for if user is already member
    if auth_user_id in channel[3]:
        raise InputError("Auth_user is already a member")

    #error checking for private channel access
    if channel[1] == False and store['global_permissions'].get(auth_user_id) != 1:
        raise AccessError("This channel is private and you do not have global permissions")

    members = channel[3]
    members.append(auth_user_id)
    
    c_name = channel[0]
    c_public = channel[1]
    c_owners = channel[2]
    c_members = members
    c_messages = channel[4]
    
    store['channels'].update({channel_id : (c_name, c_public, c_owners, c_members, c_messages)})

    return {}


def channel_leave_v1(user_id, channel_id):
    store = data_store.get()

    channel_dict = store['channels']
    if channel_id not in channel_dict.keys():
        raise InputError(description='channel_id does not refer to a valid channel') 
    
    channel_info = channel_dict[channel_id]
    if user_id not in channel_info[3]:
        raise AccessError(description='the authorised user is not a member of the channel')

    if user_id in channel_info[2]:
        channel_info[2].remove(user_id)

    channel_info[3].remove(user_id) 
    
    return {}

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    store = data_store.get()

    #check if channel_id refers to a valid channel
    if channel_id not in store['channels'].keys():
        raise InputError("channel_id does not refer to a valid channel")
    
    channel = store['channels'].get(channel_id)
    #channel_id is valid and user does not have owner permissions in channel
    if auth_user_id not in channel[3]:
        raise AccessError("Authorised user is not a member of the channel")
    
    u_permission = store['global_permissions'][auth_user_id]
    if auth_user_id not in channel[2] and u_permission != 1:
        raise AccessError("User does not have owner permission in this channel")

    #check if u_id is valid
    if u_id not in store['user_details'].keys():
        raise InputError("u_id is invalid")

    #check if u_id is not a member of channel
    
    if u_id not in channel[3]:
        raise InputError("u_id is not a member of the channel")

    #check if u_id is already an owner of the channel
    if u_id in channel[2]:
        raise InputError("User is already an owner of the channel")

    channel[2].append(u_id)
    channel[3].append(u_id)

    return {}

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    store = data_store.get()

    #check if channel_id refers to a valid channel
    if channel_id not in store['channels'].keys():
        raise InputError("channel_id does not refer to a valid channel")
    
    channel = store['channels'].get(channel_id)
    #channel_id is valid and user does not have owner permissions in channel
    if auth_user_id not in channel[3]:
        raise AccessError("Authorised user is not a member of the channel")
        
    u_permission = store['global_permissions'][auth_user_id]
    if auth_user_id not in channel[2] and u_permission != 1:
        raise AccessError("User does not have owner permissions in this channel")

    #check if u_id is valid
    if u_id not in store['user_details'].keys():
        raise InputError("u_id is invalid")

    #check if u_id is not an owner of the channel
    if u_id not in channel[2]:
        raise InputError("User is not an owner of the channel")

    #check if u_id refers to a user who is currently the only owner
    if u_id in channel[2] and len(channel[2]) == 1:
        raise InputError("User is currently the only owner of the channel")

    channel[2].remove(u_id)
    channel[3].remove(u_id)

    return {}
