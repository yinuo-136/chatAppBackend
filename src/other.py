from src.data_store import data_store

def clear_v1():
    store = data_store.get()
    store['registered_users'] = {}
    store['user_ids'] = {}
    store['logged_in_users'] = []
    store['user_details'] = {}
    store['channels'] = {}
    store['channel_members'] = {}
    store['global_permissions'] = {}
    data_store.set(store)
