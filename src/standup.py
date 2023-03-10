from src.error import InputError
from src.error import AccessError
from src.data_store import data_store
from src.user import user_details
from src.message import message_send_v1
from src.user_stats import user_stats_messages
import threading
from datetime import datetime, timezone
import time

def standup_wait_thread(length :int, u_id :int, c_id :int)->None:

    time.sleep(length) # sleep for the length of time, then send msg

    store = data_store.get()

    message_list = store['standups'][c_id]['message'] #get our standup message
    
    if len(message_list) == 0:
        message = "\n"
    else:
        message = '\n'.join(message_list)

    message_send_v1(u_id, c_id, message) #User stats already in this function

    store['standups'].pop(c_id)


def standup_create_v1(u_id :int, c_id :int, length :int)->dict:

    '''
    Parameters:     { token, channel_id, length }
    Return Type:    { time_finish }
    
    '''

    store = data_store.get()

    all_standups = store['standups']
    all_channels = store['channels']

    #InputError when any of: channel_id does not refer to a valid channel

    c_exists = (c_id in all_channels.keys())

    if (not c_exists):
        raise InputError("channel_id does not refer to a valid channel")

    #InputError when any of: length is a negative integer

    if (length < 0):
        raise InputError("length is a negative integer")

    #InputError when any of: an active standup is currently running in the channel
    
    standup_in_prog = (c_id in all_standups.keys())

    if (standup_in_prog):
        raise InputError("an active standup is currently running in the channel")

    #AccessError when: channel_id is valid and the authorised user is not a member of the channel

    members_list = all_channels[c_id][3]

    user_is_member = (u_id in members_list)

    if (not user_is_member):
        raise AccessError("channel_id is valid and the authorised user is not a member of the channel")


    # we gucci, lets begin

    

    thread = threading.Thread(target=standup_wait_thread,
                                  args=(length, u_id, c_id))
        # exits abnormally if main thread is terminated .
    thread.daemon = False
    thread.start()

    # t = Timer(length, standup_wait_thread(u_id, c_id))
    # t.start() # start our thread

    dt = datetime.now(timezone.utc)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    time_created = int(timestamp)

    time_finished = time_created + length


    all_standups[c_id] = {'time_finished' : time_finished, 'message' : [] }

    return { 'time_finish' : time_finished }



def standup_active_v1(u_id :int, c_id :int)->dict:


    #Parameters:{ token, channel_id }Return Type:{ is_active, time_finish }

    store = data_store.get()

    all_standups = store['standups']
    all_channels = store['channels']


    #InputError when: channel_id does not refer to a valid channel
    
    c_exists = (c_id in all_channels.keys())

    if (not c_exists):
        raise InputError("channel_id does not refer to a valid channel")

    # AccessError when: channel_id is valid and the authorised user is not a member of the channel

    members_list = all_channels[c_id][3]

    user_is_member = (u_id in members_list)

    if (not user_is_member):
        raise AccessError("channel_id is valid and the authorised user is not a member of the channel")


    # lets implement

    standup_in_prog = (c_id in all_standups.keys())

    is_active = False
    time_finish = None

    if (standup_in_prog):
        time_finish = all_standups[c_id]['time_finished']
        is_active = True

    return { 'is_active' : is_active,
            'time_finish' : time_finish }



def standup_send_v1(u_id :int, c_id :int, message :str)->dict:

    '''
    Parameters:     { token, channel_id, message }
    Return Type:    {}
    '''

    store = data_store.get()

    all_standups = store['standups']
    all_channels = store['channels']

    #InputError when any of: channel_id does not refer to a valid channel

    c_exists = (c_id in all_channels.keys())

    if (not c_exists):
        raise InputError("channel_id does not refer to a valid channel")

    #InputError when any of: length of message is over 1000 characters

    message_over_limit = (len(message) > 1000)

    if (message_over_limit):
        raise InputError("length of message is over 1000 characters")


    #InputError when any of: an active standup is not currently running in the channel

    standup_in_prog = (c_id in all_standups.keys())

    if (not standup_in_prog):
        raise InputError("an active standup is not currently running in the channel")
      
    
    # AccessError when: channel_id is valid and the authorised user is not a member of the channel

    members_list = all_channels[c_id][3]

    user_is_member = (u_id in members_list)

    if (not user_is_member):
        raise AccessError("channel_id is valid and the authorised user is not a member of the channel")


    # we are all g, lets continue


    curr_standup_message_list = all_standups[c_id]['message']

    username = store['user_details'][u_id][4]
    new_msg = f"{username}: {message}"

    # we append it to a list, as we join this at the end with \n
    curr_standup_message_list.append(new_msg) 

    return {}
