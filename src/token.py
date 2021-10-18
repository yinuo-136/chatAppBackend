import jwt
from src.data_store import data_store
from src.error import InputError, AccessError
from src.config import SECRET

def token_checker(token):
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
    
    store = data_store.get()
    
    # Not existent user_id
    if user_id not in store['user_details'].keys():
        raise AccessError("Invalid Token Passed: user_id does not exist")
    # User_id not logged in
    if user_id not in store['logged_in_users']:
        raise AccessError("Invalid Token Passed: user_id specified is not logged in")
    # Session_id doesnt exist
    #if session_id not in store['session_ids']:
        #raise AccessError("Invalid Token Passed: session_id does not exist")
