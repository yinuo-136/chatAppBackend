from src.error import InputError
from src.error import AccessError
from src.data_store import data_store
from datetime import datetime, timezone


def message_send_v1(user_id, channel_id, message):
    store = data_store.get()
    channel_dict = store['channels']

    if channel_id not in channel_dict.keys():
        raise InputError(description='channel_id does not refer to a valid channel')
    
    all_members = channel_dict[channel_id][3]
    if user_id not in all_members:
        raise AccessError(description='the authorised user is not a member of the channel')
    
    if len(message) < 1 or len(message) > 1000:
        raise InputError(description='length of message is less than 1 or over 1000 characters') 

    message_info = store['messages']

    #if no message in the database, set the initial one id = 1
    if message_info == {}:
        message_id = 1
    else:
        #get the last one from the message id (the largest) then + 1 to get a new id
        m_dict = list(message_info.keys())
        message_id = m_dict[-1] + 1

    #store sent time    
    dt = datetime.now(timezone.utc)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    time_created = int(timestamp)

    channel_info = channel_dict[channel_id]
    channel_info[4].append(message_id)
    
    message_info.update({message_id: [user_id, message, time_created]})
    return {'message_id': message_id}




def message_senddm_v1(user_id, dm_id, message):
    store = data_store.get()
    dm_dict = store['dms']

    if dm_id not in dm_dict.keys():
        raise InputError(description='dm_id does not refer to a valid DM')
    
    dm_info = dm_dict[dm_id]
    if user_id not in dm_info['u_ids'] and user_id not in dm_info['owner_id']:
        raise AccessError(description='the authorised user is not a member of the DM')
    
    if len(message) < 1 or len(message) > 1000:
        raise InputError(description='length of message is less than 1 or over 1000 characters') 

    message_info = store['messages']

    #if no message in the database, set the initial one id = 1
    if message_info == {}:
        message_id = 1
    else:
        #get the last one from the message id (the largest) then + 1 to get a new id
        m_dict = list(message_info.keys())
        message_id = m_dict[-1] + 1

    #store sent time    
    dt = datetime.now(timezone.utc)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    time_created = int(timestamp)

    dm_info['messages'].append(message_id)

    message_info.update({message_id: [user_id, message, time_created]})
    return {'message_id': message_id}