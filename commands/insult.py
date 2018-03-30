#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import json
import data
import bot
import form


def insult(cmd_data):
    # client = bot.get_slack_client(cmd_data.get('team_id'))
    jokes = data.load('insults.json')
    v = random.choice(jokes)
    print(json.dumps(cmd_data, indent=5))
    print("Insult: {}".format(v))


def yourmom(cmd_data):
    # client = bot.get_slack_client(cmd_data.get('team_id'))
    jokes = data.load('momma_jokes.json')
    v = random.choice(jokes)
    print(json.dumps(cmd_data, indent=5))
    print("Your Mom Joke: {}".format(v))


def add_yourmom(cmd_data):
    client = bot.get_slack_client(cmd_data.get('team_id'))
    trigger_id = cmd_data.get('trigger_id')
    msg = {
        "callback_id": form.add_yourmom.__name__,
        "title": "Add Your Own Joke!",
        "submit_label": "Go!",
        "elements": [
            {
                "type": "text",
                "label": "Joke Goes Here",
                "name": "joke_input"
            },
        ]
    }
    submit = {
        'trigger_id': trigger_id,
        'dialog': msg,
    }
    print("Submitting:")
    print(json.dumps(submit, indent=5))
    post_message = client.api_call('dialog.open', **submit)
    print("Returned:")
    print(json.dumps(post_message, indent=5))
