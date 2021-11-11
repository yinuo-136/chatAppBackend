from src.data_store import data_store
from datetime import datetime, timezone

def current_time():
    dt = datetime.now(timezone.utc)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    current_time = int(timestamp)

    return current_time

def user_stats_channels_join(u_id):
    store = data_store.get()
    channels = store['user_stats'][u_id]['channels_joined']
    num_channels = channels[-1]['num_channels_joined'] + 1

    channels.append({'num_channels_joined' : num_channels, 'time_stamp' : current_time()})

def user_stats_channels_leave(u_id):
    store = data_store.get()
    channels = store['user_stats'][u_id]['channels_joined']
    num_channels = channels[-1]['num_channels_joined'] - 1

    channels.append({'num_channels_joined' : num_channels, 'time_stamp' : current_time()})

def user_stats_dms_join(u_id):
    store = data_store.get()
    dms = store['user_stats'][u_id]['dms_joined']
    num_dms = dms[-1]['num_dms_joined'] + 1

    dms.append({'num_dms_joined' : num_dms, 'time_stamp' : current_time()})

def user_stats_dms_leave(u_id):
    store = data_store.get()
    dms = store['user_stats'][u_id]['dms_joined']
    num_dms = dms[-1]['num_dms_joined'] - 1

    dms.append({'num_dms_joined' : num_dms, 'time_stamp' : current_time()})

def user_stats_messages(u_id):
    store = data_store.get()
    messages = store['user_stats'][u_id]['messages_sent']
    num_messages = messages[-1]['num_messages_sent'] + 1

    messages.append({'num_messages_sent' : num_messages, 'time_stamp' : current_time()})
