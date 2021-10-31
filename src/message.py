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

    sent_location = ['channel', channel_id]

    shared_message = ''

    channel_info = channel_dict[channel_id]
    channel_info[4].append(message_id)

    #add the reacts
    reacts = {1:[]}
    
    message_info.update({message_id: [user_id, message, time_created, sent_location, shared_message, reacts]})
    return {'message_id': message_id}




def message_senddm_v1(user_id, dm_id, message):
    store = data_store.get()
    dm_dict = store['dms']

    if dm_id not in dm_dict.keys():
        raise InputError(description='dm_id does not refer to a valid DM')
    
    dm_info = dm_dict[dm_id]
    if user_id not in dm_info['u_ids'] and user_id != dm_info['owner_id']:
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

    sent_location = ['dm', dm_id]
    shared_message = ''

    dm_info['messages'].append(message_id)

    #add reacts
    reacts = {1:[]}
    message_info.update({message_id: [user_id, message, time_created, sent_location, shared_message, reacts]})
    return {'message_id': message_id}



def message_edit_v1(user_id, message_id, message):
    store = data_store.get()
    m_dict = store['messages']
    if message_id not in m_dict:
        raise InputError(description="message_id does not exist")
    m_location = m_dict[message_id][3]
    
    if m_location[0] == 'channel':
        c_info = store['channels'][m_location[1]]
        #check whether u_id is in the channel
        if user_id not in c_info[3]:
            raise InputError(description="message_id does not refer to a valid message within a channel/DM that the authorised user has joined")
        
        #check whether u_id has the permission to edit the message
        u_permission = store['global_permissions'][user_id]
        user_send = m_dict[message_id][0]
        if u_permission != 1 and user_id != user_send and user_id not in c_info[2]:
            raise AccessError(description="the message wasn't sent by the authorised user making this request and the authorised user does not have owner permissions in the channel/DM")    
    
    else:
        dm_info = store['dms'][m_location[1]]
        #check whether u_id is in the dm
        if user_id not in dm_info['u_ids'] and user_id != dm_info['owner_id']:
            raise InputError(description="message_id does not refer to a valid message within a channel/DM that the authorised user has joined")

        #check whether u_id has the permission to edit the message
        user_send = m_dict[message_id][0]
        if user_id != user_send and user_id != dm_info['owner_id']:
            raise AccessError(description="the message wasn't sent by the authorised user making this request and the authorised user does not have owner permissions in the channel/DM") 
         
    #check the length of the message
    if len(message) > 1000:
        raise InputError(description="length of message is over 1000 characters")
    #if message is an empty string, delete the message
    if message == '':
        if m_location[0] == 'channel':
            c_info = store['channels'][m_location[1]]
            c_info[4].remove(message_id)
        else: 
            dm_info = store['dms'][m_location[1]]
            dm_info['messages'].remove(message_id)
        m_dict.pop(message_id) 
    else:
        m_dict[message_id][1] = message  
    
    return {}



def message_remove_v1(user_id, message_id):
    store = data_store.get()
    m_dict = store['messages']
    if message_id not in m_dict:
        raise InputError(description="message_id does not exist")
    m_location = m_dict[message_id][3]
    
    if m_location[0] == 'channel':
        c_info = store['channels'][m_location[1]]
        #check whether u_id is in the channel
        if user_id not in c_info[3]:
            raise InputError(description="message_id does not refer to a valid message within a channel/DM that the authorised user has joined")
        
        #check whether u_id has the permission to edit the message
        u_permission = store['global_permissions'][user_id]
        user_send = m_dict[message_id][0]
        if u_permission != 1 and user_id != user_send and user_id not in c_info[2]:
            raise AccessError(description="the message wasn't sent by the authorised user making this request and the authorised user does not have owner permissions in the channel/DM")    
    
    else:
        dm_info = store['dms'][m_location[1]]
        #check whether u_id is in the dm
        if user_id not in dm_info['u_ids'] and user_id != dm_info['owner_id']:
            raise InputError(description="message_id does not refer to a valid message within a channel/DM that the authorised user has joined")

        #check whether u_id has the permission to edit the message
        user_send = m_dict[message_id][0]
        if user_id != user_send and user_id != dm_info['owner_id']:
            raise AccessError(description="the message wasn't sent by the authorised user making this request and the authorised user does not have owner permissions in the channel/DM") 
 
    #delete the meessage
    if m_location[0] == 'channel':
        c_info = store['channels'][m_location[1]]
        c_info[4].remove(message_id)
    else: 
        dm_info = store['dms'][m_location[1]]
        dm_info['messages'].remove(message_id)
    m_dict.pop(message_id)    
    return {} 




def message_share_v1(user_id, message_id, message, channel_id, dm_id):
    store = data_store.get() 
    c_list = store['channels']
    dm_list = store['dms']

    if channel_id not in c_list.keys() and dm_id not in dm_list.keys():
        raise InputError(description="both channel_id and dm_id are invalid")
    
    if channel_id != -1 and dm_id != -1:
        raise InputError(description="neither channel_id nor dm_id are -1")

    #check if authorised user has not joined the channel or DM they trying to share the message to
    if channel_id != -1:
        if user_id not in c_list[channel_id][3]:
            raise AccessError(description="the authorised user has not joined the channel they are trying to share the message to")
    else:
        if user_id != dm_list[dm_id]['owner_id'] and user_id not in dm_list[dm_id]['u_ids']:
            raise AccessError(description="the authorised user has not joined the DM they are trying to share the message to")

    m_dict = store['messages']
    if message_id not in m_dict:
        raise InputError(description="message_id does not exist")
    m_location = m_dict[message_id][3]
    
    if m_location[0] == 'channel':
        c_info = store['channels'][m_location[1]]
        #check whether u_id is in the channel
        if user_id not in c_info[3]:
            raise InputError(description="message_id does not refer to a valid message within a channel that the authorised user has joined")   
    
    else:
        dm_info = store['dms'][m_location[1]]
        #check whether u_id is in the dm
        if user_id not in dm_info['u_ids'] and user_id != dm_info['owner_id']:
            raise InputError(description="message_id does not refer to a valid message within a DM that the authorised user has joined")

   #check if the length of the message is more than 1000 characters
    if len(message) > 1000:
        raise  InputError(description="length of message is more than 1000 characters") 
    
    #generate a new message_id as the shared_message_id
    m_list = list(m_dict.keys())
    shared_message_id = m_list[-1] + 1

    #store sent time
    dt = datetime.now(timezone.utc)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    time_created = int(timestamp)
    shared_message = m_dict[message_id][1]
    add_message = message

    sent_location = []
    if channel_id != -1:
        sent_location = ['channel', channel_id]
        c_list[channel_id][4].append(shared_message_id)
    else:
        sent_location = ['dm', dm_id]
        dm_list[dm_id]['messages'].append(shared_message_id)
    
    #add reacts
    reacts = {1:[]}

    m_dict.update({shared_message_id: [user_id, add_message, time_created, sent_location, shared_message, reacts]})

    return {'shared_message_id': shared_message_id}


def message_react_v1(user_id, message_id, react_id):
    store = data_store.get()

    #check if message_id is not a valid message within a channel or DM that the authorised user has joined ot not
    m_dict = store['messages']
    if message_id not in m_dict:
        raise InputError(description="message_id does not exist")
    m_location = m_dict[message_id][3]
    
    if m_location[0] == 'channel':
        c_info = store['channels'][m_location[1]]
        #check whether u_id is in the channel
        if user_id not in c_info[3]:
            raise InputError(description="message_id does not refer to a valid message within a channel that the authorised user has joined")   
    
    else:
        dm_info = store['dms'][m_location[1]]
        #check whether u_id is in the dm
        if user_id not in dm_info['u_ids'] and user_id != dm_info['owner_id']:
            raise InputError(description="message_id does not refer to a valid message within a DM that the authorised user has joined")
        
    #check if react_id is a valid react ID or not
    valid_react_id = [1]
    if react_id not in valid_react_id:
        raise InputError(description="react_id is not a valid react ID")
    
    #check if the message already contains a react with ID react_id from the authorised user
    reacted_info = m_dict[message_id][5]
    reacted_users = reacted_info[react_id]
    if user_id in reacted_users:
        raise InputError(description="the message already contains a react with ID react_id from the authorised user")
    
    #add the user to the react list
    reacted_users.append(user_id)
    
    return {}

def message_unreact_v1(user_id, message_id, react_id):
    store = data_store.get()

    #check if message_id is not a valid message within a channel or DM that the authorised user has joined ot not
    m_dict = store['messages']
    if message_id not in m_dict:
        raise InputError(description="message_id does not exist")
    m_location = m_dict[message_id][3]
    
    if m_location[0] == 'channel':
        c_info = store['channels'][m_location[1]]
        #check whether u_id is in the channel
        if user_id not in c_info[3]:
            raise InputError(description="message_id does not refer to a valid message within a channel that the authorised user has joined")   
    
    else:
        dm_info = store['dms'][m_location[1]]
        #check whether u_id is in the dm
        if user_id not in dm_info['u_ids'] and user_id != dm_info['owner_id']:
            raise InputError(description="message_id does not refer to a valid message within a DM that the authorised user has joined")
        
    #check if react_id is a valid react ID or not
    valid_react_id = [1]
    if react_id not in valid_react_id:
        raise InputError(description="react_id is not a valid react ID")
    
    #check if the message does not contain a react with ID react_id from the authorised user
    reacted_info = m_dict[message_id][5]
    reacted_users = reacted_info[react_id]
    if user_id not in reacted_users:
        raise InputError(description="the message does not contain a react with ID react_id from the authorised user")    

    #pop the user to the react list
    reacted_users.remove(user_id)

    return {}



        