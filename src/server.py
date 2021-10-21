import sys
import signal
import uuid
import jwt
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.channel import channel_details_v1
from src import config
from src.dm import dm_create_v1, dm_list_v1, dm_remove_v1, dm_details_v1, dm_leave_v1, dm_messages_v1
from src.channel import channel_leave_v1, channel_messages_v1, channel_invite_v1, channel_join_v1
from src.channels import channels_listall_v1, channels_create_v1, channels_list_v1
from src.message import message_send_v1, message_senddm_v1, message_edit_v1, message_remove_v1
from src.auth import auth_login_v1, auth_register_v1, auth_logout_v1, auth_invalidate_session, auth_store_session_id
from src.user import user_details, list_all_users, user_set_email, user_set_handle, user_set_name
from src.database import save_datastore, load_datastore
from src.token import token_checker
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
    auth_store_session_id(session_id)
    
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
    auth_store_session_id(session_id)
    
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
    auth_invalidate_session(session_id)
  
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

'''   
@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_remove():
    data = request.get_json()
    
    token = data['token']
    u_id = data['u_id']
    
    token_checker(token)
    
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    auth_user_id = payload.get('user_id')
    session_id = payload.get('session_id')
    
    auth_invalidate_session(session_id)
    
    #admin_user_remove(auth_user_id, u_id)
    
    return dumps({})
'''

@APP.route("/channels/create/v2", methods=['POST'])   
def channels_create():
    #get the response from frontend
    resp = request.get_json()

    #get the dictionary from the response
    token = resp['token']
    name = resp['name']
    is_public = resp['is_public']

    #check the token validation
    token_checker(token)
    
    #decode the token
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')

    r = channels_create_v1(user_id, name, is_public)
    #persistence
    save_datastore()
    return dumps(r)


@APP.route("/channels/listall/v2", methods=['GET'])
def channels_listall():
    #get the token from frontend
    token = request.args.get('token')

    #check the token validation
    token_checker(token)

    r = channels_listall_v1()
    return dumps(r)

@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    #get the info from frontend
    resp = request.get_json()
    token = resp['token']
    channel_id = resp['channel_id']
    
    #check the token validation
    token_checker(token)

    #decode the token
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')

    #call the function
    r = channel_leave_v1(user_id,channel_id)
    #persistence
    save_datastore()
    return dumps(r)


@APP.route("/message/send/v1", methods=['POST'])
def message_send():
    resp = request.get_json()
    token = resp['token']
    channel_id = resp['channel_id']
    message = resp['message']

    #check the token validation
    token_checker(token)

    #decode the token
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')

    #call the function
    r = message_send_v1(user_id, channel_id, message)
    #persistence
    save_datastore()
    return dumps(r)


@APP.route("/channel/messages/v2", methods=['GET'])
def channel_message():
    #get the token from frontend
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))

    #check the token validation
    token_checker(token)

    #decode the token
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')

    #call the function
    r = channel_messages_v1(user_id, channel_id, start)
    return dumps(r)


@APP.route("/channel/details/v2", methods=['GET'])
#Parameters:{ token, channel_id }
#Return Type:{ name, is_public, ownder_members, all_members }
def channel_details():
    token = request.args.get('token')

    channel_id = int(request.args.get('channel_id'))

    #Token Validation
    token_checker(token)

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')

    details = channel_details_v1(user_id, channel_id)

    return dumps(details)
 
@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
    resp = request.get_json()

    token = resp['token']
    dm_id = resp['dm_id']
    message = resp['message']

    #Token Validation
    token_checker(token)

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')

    r = message_senddm_v1(user_id, dm_id, message)
    #persistence
    save_datastore()
    return dumps(r)

@APP.route("/message/edit/v1", methods=['PUT'])
def message_edit():
    resp = request.get_json()
    token = resp['token']
    message_id = resp['message_id']
    message = resp['message']

    #Token Validation
    token_checker(token)

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')

    r = message_edit_v1(user_id, message_id, message)
    #persistence
    save_datastore()
    return dumps(r)

@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    resp = request.get_json()
    token = resp['token']
    message_id = resp['message_id']

    #Token Validation
    token_checker(token)

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')

    r = message_remove_v1(user_id, message_id)
    #persistence
    save_datastore()
    return dumps(r)

	
@APP.route("/dm/create/v1", methods=['POST'])
def dm_create_http():
    '''
    
    Parameters:{ token, u_ids }
    Return Type:{ dm_id }
    
    '''
    data = request.get_json(force=True)
    
    token = data['token']
    u_ids = data['u_ids']

    token_checker(token) # will raise an error if token is invalid

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    owner_u_id = payload.get('user_id')

    
    dict_dm_id = dm_create_v1(owner_u_id, u_ids)
    dm_id = dict_dm_id['dm_id']

    return dumps({ 'dm_id' : dm_id })





@APP.route("/dm/list/v1", methods=['GET'])
def dm_list_http():
    '''
    
    Parameters:{ token }
    Return Type:{ dms }
    
    '''
    token = request.args.get('token')

    token_checker(token) # will raise an error if token is invalid

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    member_u_id = payload.get('user_id')


    dict_dms = dm_list_v1(member_u_id)
    dms = dict_dms['dms']

    return dumps({ 'dms' : dms })


@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove_http():

    '''
    Parameters:         { token, dm_id }
    Return Type:        {}
    '''

    data = request.get_json(force=True)
    
    token = data['token']
    dm_id = data['dm_id']

    token_checker(token) # will raise an error if token is invalid


    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    owner_u_id = payload.get('user_id')

    
    dm_remove_v1(owner_u_id, dm_id)
    

    return dumps( {} )



@APP.route("/dm/details/v1", methods=['GET'])
def dm_details_http():

    '''
    Parameters:     { token, dm_id }
    Return Type:    { name, members }
    '''
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))
    

    token_checker(token) # will raise an error if token is invalid


    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    owner_u_id = payload.get('user_id')

    
    payload = dm_details_v1(owner_u_id, dm_id)
    

    return dumps( payload )



@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave_http():
    '''
    
    Parameters:     { token, dm_id }
    Return Type:    {}
    
    '''
    data = request.get_json(force=True)
    
    token = data['token']
    dm_id = data['dm_id']

    token_checker(token) # will raise an error if token is invalid

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    auth_u_id = payload.get('user_id')

    
    dm_leave_v1(auth_u_id, dm_id)

    return dumps( {} )



@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages_http():

    '''
    Parameters:     { token, dm_id, start }
    Return Type:    { messages, start, end }
    '''

    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))
    start = int(request.args.get('start'))

    token_checker(token) # will raise an error if token is invalid


    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    auth_u_id = payload.get('user_id')

    
    payload = dm_messages_v1(auth_u_id, dm_id, start)
    

    return dumps( payload )
    
@APP.route("channels/list/v2", methods=['GET'])
def list_channel():
    #Token implemented 
    token = request.args.get('token')
    #token validation
    token_checker(token)
   
    r = channels_list_v1()
    return dumps(r)

@APP.route("channel/invite/v2", methods=['POST'])
def channel_invite():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    #Token Validation
    token_checker(token)
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
    channel_invite_v1(user_id, channel_id, u_id)
    dumps({})
	
@APP.route("channel/join/v2", methods=['POST'])
def channel_join():
    data = request.get_json()
    token = data('token')
    channel_id = data['channel_id']
    #Token Validation
    token_checker(token)
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
    channel_join_v1(user_id, channel_id)
    return dumps({})

'''
@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_permission_change():
    data = request.get_json()
    
    token = data['token']
    u_id = data['u_id']
    permission_id = data['permission_id']
    
    token_checker(token)
    
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    auth_user_id = payload.get('user_id')
    
    #admin_permission_change(auth_user_id, u_id, permission_id)
    
    return dumps({})
'''
#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    #load_datastore()
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
