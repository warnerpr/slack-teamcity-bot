""" some methods to handle storing slack tokens in a local file """

import os

def get_token():
    """ read token from file and return """
    with open(os.path.expanduser('~/.slackbottoken')) as token_file:
        token = token_file.read().strip()
    return token
