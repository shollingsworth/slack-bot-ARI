#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import botconfig
import bot
from flask import make_response


def process(event_data):
    if botconfig.DEBUG:
        sys.stdout.write("EVENT DATA: {}\n".format(
            json.dumps(event_data, indent=5)
        ))
        sys.stdout.flush()

    team_id = event_data.get('team_id')

    if not team_id:
        raise Exception("Error, could not extract 'team_id'")

    event = event_data.get('event')
    if not event:
        raise Exception("Error, event data empty")

    channel = event.get('channel')
    if not channel:
        raise Exception("Error, channel data invalid or empty")

    yousaid(team_id, event)
    return make_response('OK', 200)


def yousaid(team_id, event):
    client = bot.get_slack_client(team_id)
    channel = event.get('channel')
    message = event.get('text')
    if event.get('bot_id'):
        if botconfig.DEBUG:
            sys.stdout.write("You look like a bot, I'm ignoring you...\n{}\n".format(event))
        return

    send_dict = {
        'channel': channel,
        'username': botconfig.bot_name,
        'icon_emoji': botconfig.bot_emoji,
        'text': 'you said: {}'.format(message),
    }
    post_message = client.api_call("chat.postMessage", **send_dict)

    if botconfig.DEBUG:
        sys.stdout.write("SENDING: {}\n".format(
            json.dumps(send_dict, indent=5)
        ))

        sys.stdout.write("RESPONSE: {}\n".format(
            json.dumps(post_message, indent=5)
        ))
    sys.stdout.flush()
