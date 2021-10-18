import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src import config
from src.channels import token_decode, channels_create_v1

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


@APP.route("/channels/create/v2", methods=['POST'])   
def channels_create_v2():
    resp = request.get_json()
    #get the dictionary from the response
    token = resp['token']
    name = resp['name']
    is_public = resp['is_public']
    token_info = token_decode(token)
    payload = channels_create_v1(token_info[0], name, is_public)
    return dumps(payload)


#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
