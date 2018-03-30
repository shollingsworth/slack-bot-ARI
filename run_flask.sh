#!/usr/bin/env bash
export FLASK_APP=app.py
export FLASK_DEBUG=1
source ./venv/bin/activate
python -m flask run
