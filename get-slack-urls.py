#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import sys
import botconfig

# courtesy of: https://stackoverflow.com/a/7160778/7049363
url_regex = re.compile(
    r'^(?:http)s?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$',
    re.IGNORECASE,
)

usage_msg = """
Usage:
    {} <https base url>

    ------
    example: https://31248ce81234.ngrok.io
""".strip().format(os.path.basename(sys.argv[0]))


def usage(err_msg=None):
    if err_msg:
        print(err_msg)
    print(usage_msg)
    sys.exit(-1)

if len(sys.argv) == 1:
    usage("Error, I need an argument")

base = sys.argv[1]

if not re.match(url_regex, str(sys.argv[1])):
    usage("Invalid url: {}".format(base))

out = """
Slack URL Configuration Settings:

oauth/callback url:
    # "oAuth & Permissions"
    {base}/{url_oauth}
event url:
    # "Event Subscriptions"
    {base}/{url_event}
command url:
    # "Slash Commands"
    {base}/{url_command}
""".format(**{
    'base': base,
    'url_oauth': botconfig.url_oauth,
    'url_event': botconfig.url_event,
    'url_command': botconfig.url_command,
}).strip()
print(out)
