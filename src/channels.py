from src.error import InputError
from src.error import AccessError
from src.data_store import data_store


def channels_list_v1(auth_user_id):
    
    store = data_store.get()
    u_dict = store['user_details']
    
    #user id validity check
    if auth_user_id not in u_dict.keys():
    	raise AccessError("the user id you entered does not exist") 

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

def channels_listall_v1(auth_user_id):
    
    store = data_store.get()

    u_dict = store['user_details']
    # implement the user id validity check
    if auth_user_id not in u_dict.keys():
        raise AccessError("the user id you entered does not exist")

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

    store = data_store.get()

    u_dict = store['user_details']
    # implement the user id validity check
    if auth_user_id not in u_dict.keys():
        raise AccessError("the user id you entered does not exist")

    # implement the name validity check
    if len(name) < 1 or len(name) > 20:
        raise InputError("Invalid name is entered, needs to be a name between 1 and 20 characters!")
    
    #store channel information into date_store
    c_id = len(store['channels']) + 1
    owner = [auth_user_id]
    members = [auth_user_id]
    messages = {}
    store['channels'].update({c_id : (name, is_public, owner, members, messages)})
        
    return {
        'channel_id': c_id,
    }
