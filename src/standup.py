from src.error import InputError
from src.error import AccessError
from src.data_store import data_store
from src.user import user_details
import threading
import time

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

    return { 'time_finish' : 55 }