from src.error import InputError
from src.error import AccessError
from src.data_store import data_store

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    store = data_store.get()
    channel = store['channels'].get(channel_id)

    # #check if channel_id refers to a valid channel
    if channel_id not in store['channels'].keys():
        raise InputError("channel_id does not refer to a valid channel")

    # #check if auth_user_id has access to channel
    if (auth_user_id not in channel[2]) or (auth_user_id not in channel[3]):
        raise AccessError("auth_user_id does not have access to channel")

    # #provide basic details about the channel
    

    return {
        'name': 'Hayden',
        'is_public' : False,
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
    return {
    }
