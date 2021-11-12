import sys
import signal
import uuid
import jwt
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from src import config
from flask_mail import Mail, Message
from src import config
from src.dm import dm_create_v1, dm_list_v1, dm_remove_v1, dm_details_v1, dm_leave_v1, dm_messages_v1
from src.standup import standup_create_v1, standup_active_v1, standup_send_v1
from src.channel import channel_leave_v1, channel_messages_v1, channel_addowner_v1, channel_details_v1, channel_removeowner_v1, channel_invite_v1, channel_join_v1
from src.channels import channels_listall_v1, channels_create_v1, channels_list_v1
from src.message import message_send_v1, message_senddm_v1, message_edit_v1, message_remove_v1, message_share_v1, message_react_v1, message_unreact_v1, message_pin_v1, message_unpin_v1, message_send_later_channel, message_send_later_dm
from src.auth import auth_login_v1, auth_register_v1, auth_logout_v1, auth_invalidate_session, auth_store_session_id
from src.user import user_details, list_all_users, user_set_email, user_set_handle, user_set_name, user_profile_uploadphoto, user_stats_v1, users_stats_v1 
from src.notifications import notifications_get_v1
from src.database import save_datastore, load_datastore
from src.search import search_v1
from src.token import token_checker, token_generator
from src.other import clear_v1
from src.admin import admin_user_remove, admin_permission_change
from src.password import password_request_v1, password_reset_v1

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
mail = Mail(APP)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS
APP.config['MAIL_SERVER']='smtp.gmail.com'
APP.config['MAIL_PORT'] = 465
APP.config['MAIL_USERNAME'] = 'h13balpaca@gmail.com'
APP.config['MAIL_PASSWORD'] = 'comp1531'
APP.config['MAIL_USE_TLS'] = False
APP.config['MAIL_USE_SSL'] = True

mail = Mail(APP)


@APP.route("/auth/register/v2", methods=['POST'])
def register():
    data = request.get_json()    
    
    u_id = auth_register_v1(data['email'], data['password'], data['name_first'], data['name_last'])
    user_id = u_id.get('auth_user_id')
    
    #Session_id Generator
    session_id = str(uuid.uuid4())
    auth_store_session_id(user_id, session_id)
    
    #Token implementation
    token = token_generator(user_id, session_id)
    
    #Persistence
    save_datastore()
    
    return dumps({'token' : token, 'auth_user_id' : user_id})


@APP.route("/auth/login/v2", methods=['POST'])    
def login():
    data = request.get_json()
    
    u_id = auth_login_v1(data['email'], data['password'])
    user_id = u_id.get('auth_user_id')
    
    #Session_id Generator
    session_id = str(uuid.uuid4())
    auth_store_session_id(user_id, session_id)
    
    #Token implementation
    token = token_generator(user_id, session_id)
    
    save_datastore()
    return dumps({'token' : token, 'auth_user_id' : user_id})
    
@APP.route("/auth/passwordreset/request/v1", methods=['POST'])   
def request_password_change():
    data = request.get_json()
    
    email = data['email']
   
    mail.send(password_request_v1(email))
    
    save_datastore()
    return dumps({})
    

@APP.route("/auth/passwordreset/reset/v1", methods=['POST'])
def reset_password_change():
    data = request.get_json()
    
    reset_code = data['reset_code']
    new_password = data['new_password']
    
    password_reset_v1(new_password, reset_code)

    save_datastore()    
    return dumps({})
    

@APP.route("/user/profile/uploadphoto/v1", methods=['POST'])     
#Parameters:{ token, img_url, x_start, y_start, x_end, y_end }Return Type:{}
def upload_user_photo():
    data = request.get_json()
    token = data['token']
    
    token_checker(token)
    
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
    
    img_url = data['img_url']
    x_start = int(data['x_start'])
    y_start = int(data['y_start'])
    x_end = int(data['x_end'])
    y_end = int(data['y_end'])
    
    user_profile_uploadphoto(user_id, img_url, x_start, y_start, x_end, y_end)
    
    return dumps({})
    
@APP.route("/static/<path:path>")
def download_photo(path):
    return send_from_directory('static', path)

@APP.route("/message/sendlater/v1", methods=['POST'])
def sendlater_channel():
#Parameters:{ token, channel_id, message, time_sent }Return Type:{ message_id }
    data = request.get_json()
    
    #token validation
    token_checker(data['token'])
    
    channel_id = data['channel_id']
    message = data['message']
    time_sent = data['time_sent']
    
    payload = jwt.decode(data['token'], config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
    
    ret = message_send_later_channel(user_id, channel_id, message, time_sent)
    
    return dumps(ret)
    
  
@APP.route("/message/sendlaterdm/v1", methods=['POST'])
def sendlater_dm():
#Parameters:{ token, dm_id, message, time_sent }Return Type:{ message_id }
    data = request.get_json()
    
    #token validation
    token_checker(data['token'])
    
    dm_id = data['dm_id']
    message = data['message']
    time_sent = data['time_sent']
    
    payload = jwt.decode(data['token'], config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
    
    ret = message_send_later_dm(user_id, dm_id, message, time_sent)
    
    return dumps(ret)
    
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
    save_datastore()
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
    save_datastore()
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
    save_datastore()
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
    save_datastore()
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
    save_datastore()
    return dumps({})

@APP.route("/user/stats/v1", methods=['GET'])
def user_stats():
    token = request.args.get('token')
    token_checker(token)

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
    stats = user_stats_v1(user_id)

    return dumps(stats)

@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_remove():
    data = request.get_json()
    
    token = data['token']
    u_id = data['u_id']
    
    token_checker(token)
    
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    auth_user_id = payload.get('user_id')
    session_id = payload.get('session_id')
    
    admin_user_remove(auth_user_id, u_id)
    
    auth_invalidate_session(u_id, session_id)
    save_datastore()
    return dumps({})


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

@APP.route("/channel/addowner/v1", methods=['POST'])
#Parameters:{ token, channel_id, u_id } Return Type:{}
def channel_addowner():
    data = request.get_json()

    token = data['token']
    channel_id = int(data['channel_id'])
    u_id = int(data['u_id'])

    #Token Validation
    token_checker(token)

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')

    r = channel_addowner_v1(user_id, channel_id, u_id)
    save_datastore()

    return dumps(r)

@APP.route("/channel/removeowner/v1", methods=['POST'])
#Parameters:{ token, channel_id, u_id } Return Type:{}
def channel_removeowner():
    data = request.get_json()

    token = data['token']
    channel_id = int(data['channel_id'])
    u_id = int(data['u_id'])

    #Token Validation
    token_checker(token)

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')    

    r = channel_removeowner_v1(user_id, channel_id, u_id)
    save_datastore()
    
    return dumps(r)

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
    save_datastore()
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
    
    save_datastore()
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
    save_datastore()
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
    
@APP.route("/channels/list/v2", methods=['GET'])
def list_channel():
    #Token implemented 
    token = request.args.get('token')
    #token validation
    token_checker(token)

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
   
    r = channels_list_v1(user_id)
    return dumps(r)

@APP.route("/channel/invite/v2", methods=['POST'])
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
    save_datastore()
    return dumps({})
	
@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    #Token Validation
    token_checker(token)
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
    channel_join_v1(user_id, channel_id)
    save_datastore()
    return dumps({})


@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_change_permission():
    data = request.get_json()
    
    token = data['token']
    u_id = data['u_id']
    permission_id = data['permission_id']
    
    token_checker(token)
    
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    auth_user_id = payload.get('user_id')
    
    admin_permission_change(auth_user_id, u_id, permission_id)
    save_datastore()
    return dumps({})

@APP.route("/users/stats/v1", methods=['GET'])
def user_stats():
    #token implemented
    token = request.args.get('token')
    #token check 
    token_checker(token)
    
    workspace_stats = users_stats_v1()
    return dumps(workspace_stats)
    
@APP.route("/message/share/v1", methods=['POST'])
def message_share():
    data = request.get_json()

    token = data['token']
    og_message_id = data['og_message_id']
    message = data['message']
    channel_id = data['channel_id']
    dm_id = data['dm_id']

    token_checker(token)  

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    auth_user_id = payload.get('user_id')
    
    r = message_share_v1(auth_user_id, og_message_id, message, channel_id, dm_id)
    save_datastore()
    
    return dumps(r)

@APP.route("/message/react/v1", methods=['POST'])
def message_react():
    data = request.get_json()

    token = data['token']
    message_id = data['message_id']
    react_id = data['react_id']

    token_checker(token)  

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    auth_user_id = payload.get('user_id')

    r = message_react_v1(auth_user_id, message_id, react_id)
    save_datastore()

    return dumps(r)

@APP.route("/message/unreact/v1", methods=['POST'])
def message_unreact():
    data = request.get_json()

    token = data['token']
    message_id = data['message_id']
    react_id = data['react_id']

    token_checker(token)  

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    auth_user_id = payload.get('user_id')

    r = message_unreact_v1(auth_user_id, message_id, react_id)
    save_datastore()

    return dumps(r)

@APP.route("/message/pin/v1", methods=['POST'])
def message_pin():
    data = request.get_json()

    token = data['token']
    message_id = data['message_id']
   
    token_checker(token)  

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    auth_user_id = payload.get('user_id')

    r = message_pin_v1(auth_user_id, message_id)
    save_datastore()

    return dumps(r)

@APP.route("/message/unpin/v1", methods=['POST'])
def message_unpin():
    data = request.get_json()

    token = data['token']
    message_id = data['message_id']
   
    token_checker(token)  

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    auth_user_id = payload.get('user_id')

    r = message_unpin_v1(auth_user_id, message_id)
    save_datastore()

    return dumps(r)

@APP.route("/search/v1", methods=['GET'])
def search():
    #Token implemented 
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    #token validation
    token_checker(token)

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
   
    r = search_v1(user_id, query_str)
    return dumps(r)

@APP.route("/notifications/get/v1", methods=['GET'])
def notifications_get():
    #Token implemented 
    token = request.args.get('token')
    #token validation
    token_checker(token)

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
   
    r = notifications_get_v1(user_id)
    return dumps(r)


@APP.route("/standup/start/v1", methods=['POST'])
def standup_create_route():
    data = request.get_json()
    
    token = data['token']
    channel_id = data['channel_id']
    length = data['length']
    
    token_checker(token)
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    auth_user_id = payload.get('user_id')
    
    time_finish_dict = standup_create_v1(auth_user_id, channel_id, length)

    save_datastore()
    return dumps(time_finish_dict)



@APP.route("/standup/active/v1", methods=['GET'])
def standup_active_route():
    #Token implemented 
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    #token validation
    token_checker(token)

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    user_id = payload.get('user_id')
   
    r = standup_active_v1(user_id, channel_id)

    return dumps(r)



@APP.route("/standup/send/v1", methods=['POST'])
def standup_send_route():
    data = request.get_json()
    
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']
    
    token_checker(token)
    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    auth_user_id = payload.get('user_id')
    
    standup_send_v1(auth_user_id, channel_id, message)

    save_datastore()
    return dumps( {} ) # returns empty dict


#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    load_datastore()
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
