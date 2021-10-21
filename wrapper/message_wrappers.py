import pytest
import requests
from src.config import url

BASE_URL = url

def send_message(token, channel_id, message):
    payload = requests.post(f'{BASE_URL}/message/send/v1', json={'token': token,
                                                                'channel_id': channel_id,
                                                                'message': message})
    r = payload.json()
    return r['message_id']
def senddm_message(token, dm_id, message):
    payload = requests.post(f'{BASE_URL}/message/senddm/v1', json={'token': token,
                                                                'dm_id': dm_id,
                                                                'message': message})
    r = payload.json()
    return r['message_id']
def edit_message(token, message_id, message):
    payload = requests.put(f'{BASE_URL}/message/edit/v1', json={'token': token,
                                                    'message_id': message_id,
                                                    'message': message})
    return payload
def show_messages(token, channel_id, start):
    payload = requests.get(f'{BASE_URL}/channel/messages/v2', params={'token': token,
                                                                'channel_id': channel_id,
                                                                'start': start})
    p = payload.json()
    p_list = p['messages']
    temp = []
    for p_info in p_list:
        temp.append(p_info['message'])
    return temp