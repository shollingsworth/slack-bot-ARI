# -*- coding: utf-8 -*-
"""
Python Slack Bot class
"""
import sys
import os
import json
from slackclient import SlackClient
import botconfig

slack_clients = {}
slack_bot_auth_file = os.environ.get(botconfig.env_auth_file)
if not os.path.isfile(slack_bot_auth_file):
    raise Exception("Environment variable: {} holds the value of an invalid file: '{}'".format(
        botconfig.env_auth_file,
        slack_bot_auth_file,
    ))

with open(slack_bot_auth_file, 'r') as fh:
    authed_teams = json.load(fh)


def write_auth_file():
    with open(slack_bot_auth_file, 'w') as fh:
        fh.write(json.dumps(authed_teams, indent=5))


def get_bot_token(team_id):
    return authed_teams.get(team_id, {}).get('bot', {}).get('bot_access_token')


def get_bot_userid(team_id):
    return authed_teams.get(team_id, {}).get('bot', {}).get('bot_user_id')


def get_slack_client(team_id):
    token = get_bot_token(team_id)
    if not token:
        raise Exception("Error, token is not set in file: {}".format(slack_bot_auth_file))
    if team_id in slack_clients:
        return slack_clients.get(team_id)
    else:
        scli = SlackClient(token)
        res = scli.api_call('auth.test')
        if not res.get('ok'):
            raise Exception("Error authenticating: {}".format(res.get('error')))
        slack_clients[team_id] = scli
        return slack_clients[team_id]


class Bot(object):
    """ Instanciates a Bot object to handle Slack onboarding interactions."""
    def __init__(self):
        super(Bot, self).__init__()
        self.name = botconfig.bot_name
        self.emoji = botconfig.bot_emoji
        self.client_id = os.environ.get("SLACK_CLIENT_ID")
        self.client_secret = os.environ.get("SLACK_CLIENT_SECRET")
        self.verification = os.environ.get("SLACK_VERIFICATION_TOKEN")
        self.scope = "incoming-webhook,commands,bot"

        # NOTE: Python-slack requires a client connection to generate
        # an oauth token. We can connect to the client without authenticating
        # by passing an empty string as a token and then reinstantiating the
        # client with a valid OAuth token once we have one.
        self.client = SlackClient("")
        # We'll use this dictionary to store the state of each message object.
        # In a production envrionment you'll likely want to store this more
        # persistantly in  a database.
        self.messages = {}

    # Auth Callback
    def auth(self, code):
        if not code:
            raise Exception("Error, code is empty")

        auth_send = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
        }

        auth_response = self.client.api_call(
            "oauth.access",
            **auth_send
        )

        if botconfig.DEBUG:
            sys.stdout.write("AUTH SEND:\n{}\n".format(
                json.dumps(auth_send, indent=5)
            ))
            sys.stdout.write("AUTH RESPONSE:\n{}\n".format(
                json.dumps(auth_response, indent=5)
            ))

        if not auth_response.get('ok'):
            raise Exception("Error, auth response had an error: {}".format(auth_response.get('error')))

        team_id = auth_response.get('team_id')
        bot_token = auth_response["bot"]["bot_access_token"]
        authed_teams[team_id] = auth_response
        write_auth_file()
        self.client = SlackClient(bot_token)
