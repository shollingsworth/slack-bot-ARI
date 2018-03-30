#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os


def load(file_name):
    mydir = os.path.dirname(os.path.abspath(__file__))
    if os.path.isfile(file_name):
        mfile = file_name
    elif os.path.isfile(os.path.join(*[mydir, file_name])):
        mfile = os.path.join(*[mydir, file_name])
    else:
        raise Exception("Error, can't find file: {}".format(file_name))
    with open(mfile, 'r') as fh:
        return json.load(fh)
