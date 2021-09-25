from src.error import InputError
from src.error import AccessError
from src.data_store import data_store


def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
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
    store['channels'].update({c_id : (name, is_public, owner, members)})
        
    return {
        'channel_id': c_id,
    }
