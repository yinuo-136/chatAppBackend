from src.error import InputError
from src.error import AccessError
from src.data_store import data_store
from src.user_stats import user_stats_channels_join


def channels_list_v1(auth_user_id):

    store = data_store.get()

    list_dict = []
    channel_list = store['channels']
    #check whether user id given is in the owner list or members list
    for channel_id in channel_list:
    	current_channel = store['channels'].get(channel_id)
    	if auth_user_id in current_channel[3]:
            channel_name = current_channel[0]
            channel_info = {'channel_id': channel_id, 'name': channel_name,}
            #append to return type
            list_dict.append(channel_info)
            	
    #return channel id and name
    return {
    	'channels':list_dict  
    }

def channels_listall_v1():
    '''
    <this function checks the auth_user_id then return errors or the list
    of channels that have been created>
    Arguments:
    <auth_user_id> (integer)    - the unique user id

    Exceptions:
    AccessError - Occurs when the user id you entered does not exist
    
    Return Value:
    return the list of channels that have been created.   
    '''

    store = data_store.get()

    #implement the return list_all dictionary
    all_list = []
    channel_list = store['channels']
    if channel_list == {}:
        all_list = []
    else:
        for channel_id in channel_list:
            channel = channel_list.get(channel_id)
            channel_name = channel[0]
            channel_info = {'channel_id': channel_id, 'name': channel_name,}
            all_list.append(channel_info)

    return {
        'channels': all_list
    }

def channels_create_v1(auth_user_id, name, is_public):
    '''
    <create a channel based on the creator, channel name and property(public/private)>

    Arguments:
    <auth_user_id> (integer)    - user id that indicate the unique user.
    <name> (<string)    - the channel name that user want to have.
    <is_public>(boolean) -whether it's a public or private


    Exceptions:
    InputError  - Occurs when Invalid name is entered, needs to be a name between 1 and 20 characters
    AccessError - Occurs when the user id you entered does not exist

    Return Value:
    Returns a dictionary that contains channel_id that you create.
    '''
    store = data_store.get()
    # implement the name validity check
    if len(name) < 1 or len(name) > 20:
        raise InputError(description="Invalid name is entered, needs to be a name between 1 and 20 characters!")
    
    #store channel information into date_store
    c_id = len(store['channels']) + 1
    owner = [auth_user_id]
    members = [auth_user_id]
    messages = []
    store['channels'].update({c_id : (name, is_public, owner, members, messages)})

    #Analytics
    user_stats_channels_join(auth_user_id)

    return {
        'channel_id': c_id
    }

