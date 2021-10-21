import pytest
import requests
import json
from src import config
from wrapper.auth_wrappers import auth_register
from wrapper.channel_wrappers import channel_details
from wrapper.clear_wrapper import clear_http

#Waiting for channel_create to get wrapped up
def test_basic_channel_details():
    clear_http()
