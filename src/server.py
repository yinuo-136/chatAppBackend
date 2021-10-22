import sys
import signal
import uuid
import jwt
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import auth_login_v1, auth_register_v1, auth_logout_v1, auth_invalidate_session, auth_store_session_id
from src.user import user_details, list_all_users, user_set_email, user_set_handle, user_set_name
from src.data_store import data_store
from src.database import save_datastore, load_datastore
from src.token import token_checker
from src.admin import admin_permission_change, admin_user_remove
from src.other import clear_v1

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS


@APP.route("/auth/register/v2", methods=['POST'])
def register():
    data = request.get_json()    
    
    u_id = auth_register_v1(data['email'], data['password'], data['name_first'], data['name_last'])
    user_id = u_id.get('auth_user_id')
    
    #Session_id Generator
    session_id = str(uuid.uuid4())
    auth_store_session_id(user_id, session_id)
    
    payload = {
        'user_id' : user_id, 
        'session_id' :  session_id
    }
    
    #Token implementation
    token = jwt.encode(payload, config.SECRET, algorithm = 'HS256')
    
    #Persistence
    #save_datastore()
    
    return dumps({'token' : token, 'auth_user_id' : user_id})


@APP.route("/auth/login/v2", methods=['POST'])    
def login():
    data = request.get_json()
    
    u_id = auth_login_v1(data['email'], data['password'])
    user_id = u_id.get('auth_user_id')
    
    #Session_id Generator
    session_id = str(uuid.uuid4())
    auth_store_session_id(user_id, session_id)
    
    payload = {
        'user_id' : user_id, 
        'session_id' : session_id
    }
    
    #Token implementation
    token = jwt.encode(payload, config.SECRET, algorithm = 'HS256')
    
    return dumps({'token' : token, 'auth_user_id' : user_id})
    
@APP.route("/auth/logout/v1", methods=['POST'])
def logout():
    data = request.get_json()
    
    #Token Validation
    token_checker(data['token'])
    
    payload = jwt.decode(data['token'], config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
    session_id = payload.get('session_id')
     
    auth_logout_v1(user_id)
    auth_invalidate_session(user_id, session_id)
       
    return dumps({})
    
 
@APP.route("/user/profile/v1", methods=['GET'])
#Parameters:{ token, u_id }Return Type:{ user }
def profile():
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    
    #Token Validation
    token_checker(token) 
    
    user = user_details(u_id)    
    
    return dumps({
        'user' : user
    })
    


@APP.route("/users/all/v1", methods=['GET'])
#Parameters:{ token } Return Type:{ users }
def list_users():
    token = request.args.get('token')
    
    token_checker(token)
    
    users = list_all_users()
    
    return dumps({
        'users' : users
    })

# http hook for clearing the data store as per interface spec
@APP.route("/clear/v1", methods=['DELETE'])
def http_clear_req__delete():

    clear_v1()

    return dumps({})

@APP.route("/user/profile/setname/v1", methods=['PUT']) 
#Parameters:{ token, name_first, name_last } Return Type:{}
def set_user_name():
    data = request.get_json()
    
    token = data['token']
    name_first = data['name_first']
    name_last = data['name_last']
    
    #Token Validation
    token_checker(token)
    
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
    
    user_set_name(user_id, name_first, name_last)
    
    return dumps({})
    

@APP.route("/user/profile/setemail/v1", methods=['PUT'])    
#Parameters:{ token, email } Return Type:{}
def set_user_email():
    data = request.get_json()
    
    token = data['token']
    email = data['email']
    
    #Token Validation
    token_checker(token)
    
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
    
    user_set_email(user_id, email)
    
    return dumps({})
    
@APP.route("/user/profile/sethandle/v1", methods=['PUT'])   
#Parameters:{ token, handle_str } Return Type:{}
def set_user_handle():
    data = request.get_json()
    
    token = data['token']
    handle_str = data['handle_str']
    
    #Token Validation
    token_checker(token)
    
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
    
    user_set_handle(user_id, handle_str)
    
    return dumps({})
    
@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_remove_user():
    data = request.get_json()
    
    token = data['token']
    u_id = data['u_id']
    
    token_checker(token)
    
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    auth_user_id = payload.get('user_id')
    session_id = payload.get('session_id')
    
    admin_user_remove(auth_user_id, u_id)
    
    auth_invalidate_session(u_id, session_id)
    
    return dumps({})

@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_change_permissions():
    data = request.get_json()
    
    token = data['token']
    u_id = data['u_id']
    permission_id = data['permission_id']
    
    token_checker(token)
    
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    auth_user_id = payload.get('user_id')
    
    admin_permission_change(auth_user_id, u_id, permission_id)
    
    return dumps({})

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    #load_datastore()
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
