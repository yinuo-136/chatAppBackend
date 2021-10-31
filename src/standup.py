from src.error import InputError
from src.error import AccessError
from src.data_store import data_store
from src.user import user_details
from src.message import message_send_v1
import threading
from datetime import datetime, timezone

def standup_wait_thread(u_id, c_id):

    store = data_store.get()

    message = store['standups'][c_id] #get our standup message

    message_send_v1(u_id, c_id, message)

    store['standups'].pop(c_id)


def standup_create_v1(u_id, c_id, length):

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

    all_standups[c_id] = 'hey'

    t = threading.Timer(length, standup_wait_thread(u_id, c_id))
    t.start() # start our thread

    dt = datetime.now(timezone.utc)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    time_created = int(timestamp)

    time_finished = time_created + length

    return { 'time_finish' : time_finished }