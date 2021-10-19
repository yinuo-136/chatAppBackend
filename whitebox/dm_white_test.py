from src.dm import dm_create_v1, dm_list_v1, dm_remove_v1
from src.auth import auth_register_v1
from src.data_store import data_store
from src.other import clear_v1

def test_dm_create__local():

    clear_v1()

    dct_1 = auth_register_v1("test1@gmail.com", "password", "Nicholas", "Stathakis")
    u_id_1 = dct_1['auth_user_id']

    dct_2 = auth_register_v1("test2@gmail.com", "password", "Zeddy", "Zarnacle")
    u_id_2 = dct_2['auth_user_id']

    dict_dm_id = dm_create_v1(u_id_1, [u_id_2])

    dm_id = dict_dm_id['dm_id']

    assert dm_id == 1

    store = data_store.get()
    dict_dms = store['dms']

    # TODO: this is whitebox, only for testing purposes, will be moved later on
    assert dict_dms == { dm_id : {
        'name' : 'nicholasstathakis, zeddyzarnacle',
        'owner_id' : 1,
        'u_ids' : [2],
        'messages' : {},
    }}


def test_white__dm_list():

    clear_v1()

    dct_1 = auth_register_v1("test1@gmail.com", "password", "Nicholas", "Stathakis")
    u_id_1 = dct_1['auth_user_id']

    dct_2 = auth_register_v1("test2@gmail.com", "password", "Zeddy", "Zarnacle")
    u_id_2 = dct_2['auth_user_id']

    dict_dm_id = dm_create_v1(u_id_1, [u_id_2])

    dm_id = dict_dm_id['dm_id']

    assert dm_id == 1

    ret = dm_list_v1(u_id_2)
    dm = ret['dms']

    assert dm == [{'dm_id': 1, 'name': 'nicholasstathakis, zeddyzarnacle'}]


def test_white__dm_remove():

    clear_v1()


    dct_1 = auth_register_v1("test1@gmail.com", "password", "Nicholas", "Stathakis")
    u_id_1 = dct_1['auth_user_id']

    dct_2 = auth_register_v1("test2@gmail.com", "password", "Zeddy", "Zarnacle")
    u_id_2 = dct_2['auth_user_id']

    dict_dm_id = dm_create_v1(u_id_1, [u_id_2])

    dm_id = dict_dm_id['dm_id']
    


    store = data_store.get()
    dict_dms_before = store['dms']
    
    assert len(dict_dms_before) == 1

    dm_remove_v1(u_id_1, dm_id)

    store = data_store.get()
    dict_dms_after = store['dms']
    

    assert len(dict_dms_after) == 0
