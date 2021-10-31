from src.error import InputError
from src.error import AccessError
from src.data_store import data_store
from src.user import user_details
from itertools import islice


def standup_create_v1(u_id, c_id, length):

    '''
    Parameters:     { token, channel_id, length }
    Return Type:    { time_finish }
    
    '''

    store = data_store.get()

    all_standups = store['standups']
    all_channels = store['channels']

    #InputError when any of: channel_id does not refer to a valid channel



    #InputError when any of: length is a negative integer
    #InputError when any of: an active standup is currently running in the channel
      
    #AccessError when: channel_id is valid and the authorised user is not a member of the channel


    return { 'time_finish' : 55 }