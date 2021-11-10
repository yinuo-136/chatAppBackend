from src.error import InputError
from src.data_store import data_store



def get_message_info(auth_user_id ,m_id, m_dict):
    message_id = m_id
    u_id = m_dict[m_id][0]
    message = m_dict[m_id][1]
    shared_message = m_dict[m_id][4]
    time_created = m_dict[m_id][2]
    is_pinned = m_dict[m_id][6]

    #get the reacts list of the message
    react_dict = m_dict[m_id][5]
    reacts = []       
    for react_id in react_dict.keys():
        is_this_user_reacted = False
        u_ids = react_dict[react_id]
        if auth_user_id in u_ids:
            is_this_user_reacted = True
        reacts.append({'react_id': react_id,
                    'u_ids': u_ids,
                    'is_this_user_reacted': is_this_user_reacted})

    return {
            'message_id': message_id,
            'u_id': u_id,
            'message': message + shared_message,
            'time_created': time_created,
            'reacts': reacts,
            'is_pinned': is_pinned}


def search_v1(user_id, query_str):
    #raise InputError if length of query_str is less than 1 or over 1000 characters
    if len(query_str) < 1 or len(query_str) > 1000:
        raise InputError(description="length of query_str is less than 1 or over 1000 characters")
    
    message_list = []
    
    store = data_store.get()
    m_info = store['messages']
    for m_id in m_info.keys():
        full_message = m_info[m_id][1] + m_info[m_id][4]
        if query_str in full_message and m_info[m_id][0] == user_id:
            message_list.append(get_message_info(user_id, m_id, m_info))

    return {'messages': message_list} 
