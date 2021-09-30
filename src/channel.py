from src.error import InputError
from src.error import AccessError
from src.other import data_store
import src.error

def channel_invite_v1(auth_user_id, channel_id, u_id):
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
    if (auth_user_id not in channel[2]) or (auth_user_id not in channel[3]):
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
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
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


    u_id = store['user_details'].get(auth_user_id)
    #add user to channel
    members = channel[3]
    members.append(u_id)
    
    c_name = channel[0]
    c_public = channel[1]
    c_owners = channel[2]
    c_members = members
    c_messages = channel[4]
    
    store['channels'].update({channel_id : (c_name, c_public, c_owners, c_members, c_messages)})

    return {}