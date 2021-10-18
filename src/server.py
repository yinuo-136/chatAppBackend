import sys
import signal
import uuid
import jwt
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.dm import dm_create_v1, dm_list_v1
from src.token import token_checker

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

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })



@APP.route("dm/create/v1", methods=['POST'])
def dm_create_http():
    '''
    
    Parameters:{ token, u_ids }
    Return Type:{ dm_id }
    
    '''
    data = request.get_json()

    token = data['token']
    u_ids = data['u_ids']

    token_checker(token) # will raise an error if token is invalid

    payload = jwt.decode(token, config.SECRET, algorithms=["HS256"])
    owner_u_id = payload.get('user_id')



    dict_dm_id = dm_create_v1(owner_u_id, u_ids)
    dm_id = dict_dm_id['dm_id']

    return dumps({ 'dm_id' : dm_id })




@APP.route("dm/list/v1", methods=['GET'])
def dm_create_http():
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


#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
