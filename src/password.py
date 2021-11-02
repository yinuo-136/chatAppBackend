import random
import string
import hashlib
from flask_mail import Message
from src.error import InputError
from src.data_store import data_store

def user_has_a_session(user_id):
    store = data_store.get()
    
    for session in store['session_ids']:
        if session[0] == user_id:
            return True
    
    return False

    
def password_request_v1(email):
    store = data_store.get()
    
    user_id = store['user_ids'].get(email)
    
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))    
    store['unique_codes'].append((user_id, code))
    
    # invalidating the sessions / logging out the user
    if user_id != None:
        while user_has_a_session(user_id) == True:
            for i, session in enumerate(store['session_ids']):
                if session[0] == user_id:
                    store['session_ids'].pop(i)
        while user_id in store['logged_in_users']:
            store['logged_in_users'].remove(user_id)
    
    
    msg = Message(subject = 'Streams - Password Change Request', 
                  sender = 'h13balpaca@gmail.com', 
                  recipients = [email])
       
    msg.body = f" Hello Streams user,\n\n A request has been made to your account to change your password.\n Unique code: {code}\n If you did not request this change. Please ignore this email.\n\n From Streams Bot :) "
    
    data_store.set(store)
    
    return msg
    
def password_reset_v1(new_password, reset_code):
    if len(new_password) < 6:
        raise InputError("New password must be 6 or more characters")
    
    store = data_store.get()
    
    for code in store['unique_codes']:
        if reset_code == code[1]:
            user_id = code[0]
            break
    else:
        raise InputError("The provided code is not a valid reset code")
        
    user = store['user_details'].get(user_id)
    store['user_details'].update({user_id : (user[0], hashlib.sha256(new_password.encode()).hexdigest(), user[2], user[3], user[4], user[5])})
    u_email = user[0]
    
    store['registered_users'].update({u_email : hashlib.sha256(new_password.encode()).hexdigest()})
    
    data_store.set(store)
