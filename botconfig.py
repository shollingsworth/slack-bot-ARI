#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

# turn this on if you need more info from flask
DEBUG = True

# Basic bot name / emoji
bot_name = "Annoying Repeating Insult Bot"
bot_emoji = ":robot_face:"

# randomize these... or don't
url_oauth = 'rHLNr2iBeCIoK'
url_command = 'kFl0hkZ4hFBZffWP'
url_event = 'n3eTuYXk2Hzhea'

# Environment Variable Names
env_auth_file = 'SLACK_BOT_AUTH_FILE'
env_client_id = 'SLACK_CLIENT_ID'
env_verification_token = 'SLACK_VERIFICATION_TOKEN'
env_client_secret = 'SLACK_CLIENT_SECRET'


check_bad_environments = [
    env_auth_file,
    env_verification_token,
    env_client_id,
    env_client_secret,
]

for var in check_bad_environments:
    if not os.environ.get(var):
        raise Exception("Error, environment variable: {} is not set".format(var))
