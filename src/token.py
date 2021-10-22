import jwt
from src.data_store import data_store
from src.error import InputError, AccessError
from src.config import SECRET

def token_checker(token):
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
    session_id = payload.get('session_id')
    
    store = data_store.get()
    
    # User_id check
    if user_id not in store['user_details'].keys():
        raise AccessError("Invalid Token Passed: user_id specified doesn't exist")
    # User_id not logged in
    if user_id not in store['logged_in_users']:
        raise AccessError("Invalid Token Passed: user_id specified is not logged in")
   
    # Session_id exist check
    for session in store['session_ids']:
        if session[0] == user_id and session[1] == session_id:
            return
    
    raise AccessError("Invalid Token Passed: session_id does not exist")
