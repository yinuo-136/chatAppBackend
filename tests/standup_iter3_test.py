from typing import Any
import requests
import json
import jwt
from requests.api import request
from src import config
from src.other import clear_v1

from wrapper.standup_wrappers import standup_create
from wrapper.auth_wrappers import auth_register
from wrapper.message_wrappers import senddm_message
from wrapper.clear_wrapper import clear_http


def test_standup_start__success__basic():

    # Clear

    clear_http()

    # Register a user

    # create a channel

    # start a standup

    # check it returns 200 OK and a time_finish
