'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''

## YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'registered_users' : {},
    'user_ids': {},
    'logged_in_users' : [],
    'user_details' : {},
    'channels' : {},
    'global_permissions' : {},
    'session_ids' : [],
    'dms' : {},
    'messages' : {},
    'workspace_stats' : {
        'channels_exist' : [{'num_channels_exist','time_stamp'}],
        'dms_exist': [{'num_dms_exist','time_stamp'}],
        'messages_exist': [{'num_messages_exist','time_stamp'}],
        'utilization_rate'
    },
    'notifications': {},
    'standups' : {},
    'unique_codes' : [],
    'user_stats' : {},
    'workspace_stats' : {},
>>>>>>> 1cdcefefffc537ba6658608ee16baa7454792292
}
## YOU SHOULD MODIFY THIS OBJECT ABOVE

class Datastore:
    def __init__(self):
        self.__store = initial_object

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

print('Loading Datastore...')

global data_store
data_store = Datastore()

