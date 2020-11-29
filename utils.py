import json

from datetime import datetime


def read_json(name):
    with open('{}.json'.format(name)) as json_file:
        data = json.load(json_file)
    return data


def current_time():
    return '[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ']'
