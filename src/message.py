import threading
import time
from src.error import InputError
from src.error import AccessError
from src.data_store import data_store
from datetime import datetime, timezone
from src.notifications import notification_tag, update_notification_channel, update_notification_dm, update_react_notification
from src.user_stats import user_stats_messages
from src.stats import stats_message_send, stats_update_utilization
from typing import List, Dict, Union 

def message_send_v1(user_id :int, channel_id :int, message :str)->dict:
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
    reacts :dict = {1:[]}

    #add the is_pinned attribute
    is_pinned = False
    

    
    message_info.update({message_id: [user_id, message, time_created, sent_location, shared_message, reacts, is_pinned]})

    #notification implementation
    #check if there is tags in the message
    if "@" in message:
        handle_list = notification_tag(message)

        #construct the notification message
        user_info = store['user_details']
        user_handle = user_info[user_id][4]
        channel_name = channel_info[0]
        n_message = message[0:20]
        notification_message = f"{user_handle} tagged you in {channel_name}: {n_message}"
        n_dict = {'channel_id': channel_id, 'dm_id': -1, 'notification_message': notification_message}

        #update the notification dict
        update_notification_channel(store, handle_list, n_dict, channel_id)
	
    #user/stats helper function calls
    stats_message_send()

    #Analytics
    user_stats_messages(user_id)

    return {'message_id': message_id}



def message_senddm_v1(user_id :int, dm_id :int, message :str)->dict:
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
    reacts :dict = {1:[]}

    #add the is_pinned attribute
    is_pinned = False

    message_info.update({message_id: [user_id, message, time_created, sent_location, shared_message, reacts, is_pinned]})

    #notification implementation
    #check if there is tags in the message
    if "@" in message:
        handle_list = notification_tag(message)

        #construct the notification message
        user_info = store['user_details']
        user_handle = user_info[user_id][4]
        dm_name = dm_info['name']
        n_message = message[0:20]
        notification_message = f"{user_handle} tagged you in {dm_name}: {n_message}"
        n_dict = {'channel_id': -1, 'dm_id': dm_id, 'notification_message': notification_message}

        #update the notification dict
        update_notification_dm(store, handle_list, n_dict, dm_id)

    #Analytics
    user_stats_messages(user_id)
    
    #user/stats helper function calls
    stats_message_send()

    return {'message_id': message_id}



def message_edit_v1(user_id :int, message_id :int, message :str)->dict:
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

        #notification implementation
        #check if there is tags in the message
        if "@" in message:
            handle_list = notification_tag(message)
            user_info = store['user_details']
            user_handle = user_info[user_id][4]
            if m_location[0] == 'channel':
                #construct the notification message
                channel_name = c_info[0]
                n_message = message[0:20]
                notification_message = f"{user_handle} tagged you in {channel_name}: {n_message}"
                n_dict = {'channel_id': m_location[1], 'dm_id': -1, 'notification_message': notification_message}

                #update the notification dict
                update_notification_channel(store, handle_list, n_dict, m_location[1])  
            else: 
                #construct the notification message              
                dm_name = dm_info['name']
                n_message = message[0:20]
                notification_message = f"{user_handle} tagged you in {dm_name}: {n_message}"
                n_dict = {'channel_id': -1, 'dm_id': m_location[1], 'notification_message': notification_message}

                #update the notification dict
                update_notification_dm(store, handle_list, n_dict, m_location[1])
    
    return {}



def message_remove_v1(user_id :int, message_id :int)->dict:
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
    #user/stats helper function calls
    stats_message_send() 
    return {} 


def message_share_v1(user_id :int, message_id :int, message :str, channel_id :int, dm_id :int)->dict:
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
    reacts :dict = {1:[]}

    #add the is_pinned attribute
    is_pinned = False

    m_dict.update({shared_message_id: [user_id, add_message, time_created, sent_location, shared_message, reacts, is_pinned]})

    #notification implementation
    #check if there is tags in the message
    if "@" in message:
        handle_list = notification_tag(message)
        user_info = store['user_details']
        user_handle = user_info[user_id][4]
        if m_location[0] == 'channel':
            #construct the notification message
            channel_name = c_info[0]
            n_message = message[0:20]
            notification_message = f"{user_handle} tagged you in {channel_name}: {n_message}"
            n_dict = {'channel_id': m_location[1], 'dm_id': -1, 'notification_message': notification_message}

            #update the notification dict
            update_notification_channel(store, handle_list, n_dict, m_location[1])  
        else: 
            #construct the notification message              
            dm_name = dm_info['name']
            n_message = message[0:20]
            notification_message = f"{user_handle} tagged you in {dm_name}: {n_message}"
            n_dict = {'channel_id': -1, 'dm_id': m_location[1], 'notification_message': notification_message}

            #update the notification dict
            update_notification_dm(store, handle_list, n_dict, m_location[1])

    return {'shared_message_id': shared_message_id}





def message_react_v1(user_id :int, message_id :int, react_id :int)->dict:
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

    #notification implementation
    user_info = store['user_details']
    user_handle = user_info[user_id][4]
    if m_location[0] == 'channel':
        #construct the notification message
        channel_name = c_info[0]
        notification_message = f"{user_handle} reacted to your message in {channel_name}"
        n_dict = {'channel_id': m_location[1], 'dm_id': -1, 'notification_message': notification_message}
  
    else: 
        #construct the notification message              
        dm_name = dm_info['name']
        notification_message = f"{user_handle} reacted to your message in {dm_name}"
        n_dict = {'channel_id': -1, 'dm_id': m_location[1], 'notification_message': notification_message}
    update_react_notification(store, n_dict, message_id)
    return {}

def message_unreact_v1(user_id :int, message_id :int, react_id :int)->dict:
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

    #remove the user from the react list
    reacted_users.remove(user_id)

    return {}

def message_pin_v1(user_id :int, message_id :int)->dict:
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
        
        #check whether u_id has the owner permission to pin the message
        u_permission = store['global_permissions'][user_id]
        if u_permission != 1 and user_id not in c_info[2]:
            raise AccessError(description="the authorised user does not have owner permissions in the channel")    
    
    else:
        dm_info = store['dms'][m_location[1]]
        #check whether u_id is in the dm
        if user_id not in dm_info['u_ids'] and user_id != dm_info['owner_id']:
            raise InputError(description="message_id does not refer to a valid message within a DM that the authorised user has joined")

        #check whether u_id has the permission to pin the message
        if user_id != dm_info['owner_id']:
            raise AccessError(description="the authorised user does not have owner permissions in the DM") 

    #check if the message is already pinned   
    if m_dict[message_id][6]:
        raise InputError(description="the message is already pinned")

    #pin the message
    m_dict[message_id][6] = True

    return {}

def message_unpin_v1(user_id :int, message_id :int)->dict:
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
        
        #check whether u_id has the owner permission to pin the message
        u_permission = store['global_permissions'][user_id]
        if u_permission != 1 and user_id not in c_info[2]:
            raise AccessError(description="the authorised user does not have owner permissions in the channel")    
    
    else:
        dm_info = store['dms'][m_location[1]]
        #check whether u_id is in the dm
        if user_id not in dm_info['u_ids'] and user_id != dm_info['owner_id']:
            raise InputError(description="message_id does not refer to a valid message within a DM that the authorised user has joined")

        #check whether u_id has the permission to pin the message
        if user_id != dm_info['owner_id']:
            raise AccessError(description="the authorised user does not have owner permissions in the DM") 

    #check if the message is already pinned   
    if m_dict[message_id][6] == False:
        raise InputError(description="the message is not already pinned")

    #pin the message
    m_dict[message_id][6] = False

    return {}

    



        
def send_later_helper_channel(channel_id, message_id, message, user_id):
    store = data_store.get()

    #notification implementation
    #check if there is tags in the message
    channel_info = store['channels'][channel_id]
    if "@" in message:
        handle_list = notification_tag(message)

        #construct the notification message
        user_info = store['user_details']
        user_handle = user_info[user_id][4]
        channel_name = channel_info[0]
        n_message = message[0:20]
        notification_message = f"{user_handle} tagged you in {channel_name}: {n_message}"
        n_dict = {'channel_id': channel_id, 'dm_id': -1, 'notification_message': notification_message}

        #update the notification dict
        update_notification_channel(store, handle_list, n_dict, channel_id)
    
    channel = store['channels'].get(channel_id)
    channel[4].append(message_id)
    
    #Analytics
    user_stats_messages(user_id)

    #user/stats helper function call
    stats_message_send()

    data_store.set(store)

def message_send_later_channel(user_id :int, channel_id :int, message :str, time_sent :int) ->dict:
    store = data_store.get()
    
    if channel_id not in store['channels'].keys():
        raise InputError("The channel does not exist!")
    
    if len(message) > 1000:
        raise InputError("The message you are sending is too long. (Must be < 1000 chars)")
     
    dt = datetime.now(timezone.utc)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    current_time = int(timestamp)   
    
    if time_sent < current_time:
        raise InputError("Invalid time specified: Cannot send message in the past")
        
    #Create the message but do not send to channel 
    ############################################## 
    #if no message in the database, set the initial one id = 1
    if store['messages'] == {}:
        message_id = 1
    else:
        #get the last one from the message id (the largest) then + 1 to get a new id
        m_ids = list(store['messages'].keys())
        message_id = m_ids[-1] + 1
        
    sent_location = ['channel', channel_id]

    shared_message = ''

    #add the reacts
    reacts :dict = {1:[]}

    #add the is_pinned attribute
    is_pinned  = False

           
    store['messages'].update({message_id: [user_id, message, time_sent, sent_location, shared_message, reacts, is_pinned]})    
        
    time_until_send = time_sent - current_time
    
    t = threading.Timer(time_until_send, send_later_helper_channel, [channel_id, message_id, message, user_id])
    t.start()
    
    return {'message_id': message_id} 
    
def send_later_helper_dm(dm_id, message_id, message, user_id):
    store = data_store.get()

    dm_info = store['dms'][dm_id]
    #notification implementation
    #check if there is tags in the message
    if "@" in message:
        handle_list = notification_tag(message)

        #construct the notification message
        user_info = store['user_details']
        user_handle = user_info[user_id][4]
        dm_name = dm_info['name']
        n_message = message[0:20]
        notification_message = f"{user_handle} tagged you in {dm_name}: {n_message}"
        n_dict = {'channel_id': -1, 'dm_id': dm_id, 'notification_message': notification_message}

        #update the notification dict
        update_notification_dm(store, handle_list, n_dict, dm_id)

    dm = store['dms'].get(dm_id)
    dm['messages'].append(message_id)
    
    #Analytics
    user_stats_messages(user_id)

    #user/stats helper function calls
    stats_message_send()
    
    data_store.set(store)
    
def message_send_later_dm(user_id :int, dm_id :int, message :str, time_sent :int)->dict:
    #{ "dms" : { "dm_id" : {'name' : 'a, b, c', owner_id' : 1, 'u_ids': [2,3,4], 'messages' : [] } } }
    store = data_store.get()
    
    if dm_id not in store['dms'].keys():
        raise InputError("That dm does not exist!")
    
    if len(message) > 1000:
        raise InputError("The message you are sending is too long. (Must be < 1000 chars)")
     
    dt = datetime.now(timezone.utc)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    current_time = int(timestamp)   
    
    if time_sent < current_time:
        raise InputError("Invalid time specified: Cannot send message in the past")
        
    #Create the message but do not send to channel 
    ############################################## 
    #if no message in the database, set the initial one id = 1
    if store['messages'] == {}:
        message_id = 1
    else:
        #get the last one from the message id (the largest) then + 1 to get a new id
        m_ids = list( store['messages'].keys())
        message_id = m_ids[-1] + 1
        
    sent_location = ['dm', dm_id]

    shared_message = ''

    #add reacts
    reacts :dict = {1:[]}

    #add the is_pinned attribute
    is_pinned = False     
    store['messages'].update({message_id: [user_id, message, time_sent, sent_location, shared_message, reacts, is_pinned]})    
        
    time_until_send = time_sent - current_time
    
    t = threading.Timer(time_until_send, send_later_helper_dm, [dm_id, message_id, message, user_id])
    t.start()

    
    return {'message_id': message_id} 
