import jwt
from src.data_store import data_store
from src.error import InputError, AccessError
from src.config import SECRET

def token_generator(auth_user_id, session_id):
    payload = {
        'user_id' : auth_user_id, 
        'session_id' :  session_id
    }
    
    return jwt.encode(payload, SECRET, algorithm = 'HS256')


def token_checker(token):
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
    session_id = payload.get('session_id')
    
    store = data_store.get()
    
    # User_id check
    if user_id not in store['user_details'].keys():
        raise AccessError("Invalid Token Passed: user_id specified doesn't exist")
   
    # Session_id exist check
    for session in store['session_ids']:
        if session[0] == user_id and session[1] == session_id:
            return
    
    raise AccessError("Invalid Token Passed: session_id does not exist")

        
    
        
