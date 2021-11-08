from src.data_store import data_store

def clear_v1():
    store = data_store.get()
    
    store['registered_users'] = {}
    store['user_ids'] = {}
    store['logged_in_users'] = []
    store['user_details'] = {}
    store['channels'] = {}
    store['global_permissions'] = {}
    store['session_ids'] = []
    store['dms'] = {}
    store['messages'] = {}
    store['notifications'] = {}
    store['standups'] = {}
    store['unique_codes'] = []
    store['user_stats'] = {}
    store['workspace_stats'] = {}
    
    data_store.set(store)
    return {}
