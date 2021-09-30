from src.error import InputError
from src.error import AccessError
from src.data_store import data_store

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    store = data_store.get()

    #check if auth_user_id is valid
    if auth_user_id not in store['user_details'].keys():
        raise AccessError("user_id is invalid")

    #check if channel_id refers to a valid channel
    if channel_id not in store['channels'].keys():
        raise InputError("channel_id does not refer to a valid channel")

    #check if auth_user_id has access to channel
    channel = store['channels'].get(channel_id)
    if (auth_user_id not in channel[2]) or (auth_user_id not in channel[3]):
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


    #since at this stage that messages can not be added, so the function can only raise errors
    #or return empty message lists, thus this return won't be used.
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
