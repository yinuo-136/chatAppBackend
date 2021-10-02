from src.error import InputError
from src.error import AccessError
from src.data_store import data_store

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

    #check auth_user_id is valid
    if auth_user_id not in store['user_details'].keys():
        raise AccessError()

    #check channel_id is valid
    if channel_id not in store['channels'].keys():
        raise InputError()

    #check u_id is valid
    if u_id not in store['user_details'].keys():
        raise InputError()

    #check u_id is already member of channel_details_v1
    channel = store['channels'].get(channel_id)
    if (u_id in channel[2]) or (u_id in channel[3]):
        raise InputError()

    #check whether auth_user_id is a member of the channel
    if auth_user_id not in channel[3]:
        raise AccessError()

    
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

    #check if auth_user_id is valid
    if auth_user_id not in store['user_details'].keys():
        raise AccessError("user_id is invalid")

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
        'all_members': members,
    }


def channel_messages_v1(auth_user_id, channel_id, start):
    '''
    <return 50 messages from the start point in a channel>

    Arguments:
        <auth_user_id> (integer)    - user id
        <channel_id> (integer)    -channel_id
        <start> (integer)     - the start point where the messages should be cllected from
    
    Exceptions:
        InputError  - Occurs when 1. channel_id does not refer to a valid channel
                                  2. start number is less than to zero  
                                  3. start is greater than the total number of messages in the channel
        AccessError - Occurs when 1. the user id you entered does not exist
                                  2. the authorised user is not a member of the channel
                                  
    Return Value:
        Only return an empty list of channels at this stage since messages can not be added.
    '''

    store = data_store.get()

    u_dict = store['user_details']
    # implement the user id validity check
    if auth_user_id not in u_dict.keys():
        raise AccessError("the user id you entered does not exist")
    
    #implement the channel id validity check
    c_dict = store['channels']
    if channel_id not in c_dict.keys():
        raise InputError("channel_id does not refer to a valid channel")

    #implement the user membership check
    c_info = c_dict[channel_id]
    c_members = c_info[3]
    if auth_user_id not in c_members:
        raise AccessError("the authorised user is not a member of the channel")

    #implement the start number check
    c_messages = c_info[4]

    if start < 0 :
        raise InputError("start number needs to be greater ot equal to zero")

    if len(c_messages) < start:
        raise InputError("start is greater than the total number of messages in the channel")
    
    if c_messages == {}:
        return { 'messages': [], 'start': 0, 'end': -1}


    #since at this stage that messages can not be added, so the function can only raise errors or return empty message lists, thus this return won't be used.
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
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

    #check for valid auth_user_id
    if auth_user_id not in store['user_details'].keys():
        raise AccessError()


    #error checking for invalid channel_id
    if channel_id not in store['channels'].keys():
        raise InputError()


    #error checking for if user is already member
    if auth_user_id in channel[2]:
        raise InputError()
    elif auth_user_id in channel[3]:
        raise InputError()

    #error checking for private channel access
    if channel[1] == False and store['global_permissions'].get(auth_user_id) != 1:
        raise AccessError()

    members = channel[3]
    members.append(auth_user_id)
    
    c_name = channel[0]
    c_public = channel[1]
    c_owners = channel[2]
    c_members = members
    c_messages = channel[4]
    
    store['channels'].update({channel_id : (c_name, c_public, c_owners, c_members, c_messages)})

    return {}
