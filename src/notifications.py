from src.data_store import data_store
from typing import List, Dict, Union

def notification_tag(message :str)->List[str]:
    handle_list = []
    temp_handle = ''

    #initialize the state to 0
    state = 0
    for char in message:
        #if @ char is found, change state to 1
        if char == '@':
            state = 1
            continue
        if state == 1:
            #add the character into the temp_handle if the state is 1 and char is alphanumeric.
            if char.isalnum():
                temp_handle = temp_handle + char
            else:
                state = 0
                handle_list.append(temp_handle)
                temp_handle = ''
    #ensure the last tagged person is add to the list
    handle_list.append(temp_handle)
    
    return handle_list

def update_notification_channel(store, handle_list, n_dict, channel_id):
        #update the notification dict
        user_info = store['user_details']
        channel_member = store['channels'][channel_id][3]
        for tag_handle in handle_list:
            for user_detail in user_info.items(): 
                if user_detail[1][4] == tag_handle and user_detail[0] in channel_member :
                    if user_detail[0] not in store['notifications']:
                        store['notifications'].update({user_detail[0]: [n_dict]})
                    else:
                        store['notifications'][user_detail[0]].append(n_dict)

def update_notification_dm(store, handle_list, n_dict, dm_id):
    #update the notification dict
    user_info = store['user_details']
    dm_info = store['dms'][dm_id]
    for tag_handle in handle_list:
        for user_detail in user_info.items(): 
            if user_detail[1][4] == tag_handle:
                if user_detail[0] in dm_info['u_ids'] or user_detail[0] == dm_info['owner_id']:
                    if user_detail[0] not in store['notifications']:
                        store['notifications'].update({user_detail[0]: [n_dict]})
                    else:
                        store['notifications'][user_detail[0]].append(n_dict)
                    
def update_react_notification(store, n_dict, m_id):
    #update the notification dict
    u_id = store['messages'][m_id][0]
    if u_id not in store['notifications']:
        store['notifications'].update({u_id: [n_dict]}) 
    else:
        store['notifications'][u_id].append(n_dict)


def notifications_get_v1(u_id :int)->dict:
    store = data_store.get()
    n_info = store['notifications']
    if u_id not in n_info:
        notifications = []
    else:
        r_n_info = list(reversed(n_info[u_id]))
        notifications = r_n_info[0 : 20]
    
    return {'notifications': notifications}

    
