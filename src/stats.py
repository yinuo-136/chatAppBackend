from src.data_store import data_store
from datetime import datetime, timezone

def current_time():
    dt = datetime.now(timezone.utc)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    current_time = int(timestamp)
    
    return current_time
   
def stats_channel_create():
    store = data_store.get()
    
    channels_exist = store["workspace_stats"]["channels_exist"]
    
    num_channels = len(store['channels'])
    
    channels_exist.append({
        'num_channels_exist' : num_channels,
        'time_stamp' : current_time()
    })
    
def stats_dm_create():
	store = data_store.get()
	
	dms_exist = store["workspace_stats"]["dms_exist"]
	
	num_dms = len(store['dms'])
	
	dms_exist.append({
		'num_dms_exist' : num_dms,
		'time_stamp' : current_time()
	})

def stats_message_send():
	store = data_store.get()
	messages_exist = store["workspace_stats"]["messages_exist"]
	
	num_messages = len(store['messages'])
	
	messages_exist.append({
	    'num_messages_exist' : num_messages,
	    'time_stamp' : current_time()
	})
	
def stats_update_utilization():
    #rate = num_users_who_have_joined_at_least_one_channel_or_dm / num_users
    
    store = data_store.get()
    
    num_users = len(store['user_details'])
    
    joined_users = []
    
    for channel in store['channels'].values():
        members = channel[3]
        for u_id in members:
            if u_id is not in joined_users:
                joined_users.append(u_id)
    
    for dm in store['dms'].values():
        members = dm['u_ids']
        for u_id in members:
            if u_id is not in joined_users:
                joined_users.append(u_id)

    num_joined_users = len(joined_users)
    
    new_rate = num_joined_users / num_users
    
    store["workspace_stats"].update({"utilization_rate" : new_rate})
    
    data_store.set(store)
