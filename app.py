# -*- coding: utf-8 -*-
"""
based on: https://github.com/slackapi/Slack-Python-Onboarding-Tutorial
Steven Hollingsworth / shollingsworth@barracuda.com
"""
import json
import sys
import botconfig
import bot
import event
import commands
import form
from flask import Flask, request, make_response, render_template

# obsfucate , not fantastic, but this might keep the skids out
pyBot = bot.Bot()
app = Flask(__name__)

cmd_sento_function = {
    '/yourmom': commands.insult.yourmom,
    '/yourmom_add': commands.insult.add_yourmom,
    '/insult': commands.insult.yourmom,
}


# Process form input
@app.route("/form", methods=["POST"])
def formprocess():
    data = request.form.getlist('payload')
    data = [json.loads(i) for i in data][0]
    callback = data.get('callback_id')
    try:
        cb_func = getattr(form, callback)
    except AttributeError:
        return make_response("Whatchu talkin' about Willis?", 510)
    except Exception as e:
        return make_response("Fuck... I don't know what I'm doing here?", 511)
        # debug log something or other @TODO
        print("Exception: {}".format(e.message))
    cb_func(data)
    return make_response('', 200)


@app.route("/cmd", methods=["POST"])
def docmd():
    data = request.form
    if not data:
        raise Exception("Error, data is empty in request")
    # @TODO Moar validation
    cmd = data.get('command')
    if cmd not in cmd_sento_function.keys():
        raise Exception("Error, {} not found in configuration")
    cmd_sento_function[cmd](data)
    return make_response('', 200)


# This will be put under Redirect URLs under the oAuth section for you app
# Example https://blarg.com/{callback_url} , https is required
@app.route("/callback", methods=["GET", "POST"])
def callback():
    # Let's grab that temporary authorization code Slack's sent us from
    # the request's parameters.
    code_arg = request.args.get('code')
    if not code_arg:
        raise Exception(
            "Error, code not specified during oauth setup, see: {}".format(
                'https://api.slack.com/docs/slack-button',
            )
        )
    # The bot's auth method to handles exchanging the code for an OAuth token
    pyBot.auth(code_arg)
    return render_template("thanks.html")


# This is pretty simple, pretty much a static html page based on class varibles
@app.route("/install", methods=["GET"])
def pre_install():
    """This route renders the installation page with 'Add to Slack' button."""
    return render_template(
        "install.html",
        bot_name=botconfig.bot_name,
        client_id=pyBot.client_id,
        scope=pyBot.scope,
    )


@app.route("/event", methods=["GET", "POST"])
def hears():
    """
    This route listens for incoming events from Slack and uses the event
    handler helper function to route events to our Bot.
    """
    if request.data:
        slack_event = json.loads(request.data)
    elif request.form:
        slack_event = json.loads(request.form)
    else:
        raise Exception("Error, request.data/form not present")
    sys.stdout.flush()

    # ============= Slack URL Verification ============ #
    # In order to verify the url of our endpoint, Slack will send a challenge
    # token in a request and check for this token in the response our endpoint
    # sends back.
    #       For more info: https://api.slack.com/events/url_verification
    if "challenge" in slack_event:
        return make_response(
            slack_event["challenge"],
            200,
            {"content_type": "application/json"},
        )

    # ============ Slack Token Verification =========== #
    # We can verify the request is coming from Slack by checking that the
    # verification token in the request matches our app's settings
    if pyBot.verification != slack_event.get("token"):
        err_msg = "Invalid Slack verification token: {}\n\npyBot has: {}\n\n".format(
            slack_event["token"],
            pyBot.verification
        )
        # By adding "X-Slack-No-Retry" : 1 to our response headers, we turn off
        # Slack's automatic retries during development.
        make_response(err_msg, 403, {"X-Slack-No-Retry": 1})

    # ====== Process Incoming Events from Slack ======= #
    # If the incoming request is an Event we've subcribed to
    if "event" in slack_event:
        return event.process(slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    msg = "[NO EVENT IN SLACK REQUEST] These are not the droids you're looking for."
    return make_response(msg, 404, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
    app.run(debug=True)
