""" sanity test for the slack api, 

    just call their test API, which at least tests authentication and that
    they are up
"""

import os
import json
import requests

import slacktoken

def test_api(token):
    params = {'token': token}
    url = 'https://slack.com/api/auth.test'
    resp = requests.get(url, params=params)
    print resp.content

def main():
    token = slacktoken.get_token()
    test_api(token)


if __name__ == '__main__':
    main()
