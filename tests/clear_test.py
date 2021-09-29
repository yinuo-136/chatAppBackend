import pytest

from src.other import clear_v1
from src.data_store import *


def test_basic_clear__set():

    store = data_store.get()
    store['registered_users'] = {"Some", "Information"}
    data_store.set(store)

    clear_v1()

    store = data_store.get()

    assert store['registered_users'] == {}



def test_basic_clear__append():

    store = data_store.get()
    store['logged_in_users'].append("Gerald")

    clear_v1()

    store = data_store.get()

    assert store['logged_in_users'] == []


def test_full_clear():

    store = data_store.get()

    store['registered_users'] = {"Person1", "Person2"}
    store['user_ids'] = {1, 2}
    store['logged_in_users'] = ["Person2"]
    store['user_details'] = {"Lives in Galactron, 18th Crescent", "Has three legs"}
    store['channels'] = {"Channel1", "Channel2"}
    store['global_permissions'] = {None}

    data_store.set(store)

    clear_v1()

    store = data_store.get()

    print(store)

    assert store == {
        'registered_users' : {}, 
        'user_ids': {}, 
        'logged_in_users' : [], 
        'user_details' : {}, 
        'channels' : {}, 
        'global_permissions' : {},
        }
