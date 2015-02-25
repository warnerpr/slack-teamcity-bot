slack-teamcity-bot
==================

A slack bot that watches for [TeamCity](https://www.jetbrians.com/teamcity/) links, and dumps some info into [Slack](https://slack.com/) when it sees them.  The output is intended to match that of https://github.com/PeteGoo/tcSlackBuildNotifier   The key difference is that this bot watches for TeamCity links to fly by and then follows them, rather than pushing notifications from TeamCity, which is also useful, but covered by the linked project.

Limitations:
------------
 - error handling on the API side is non existant so far, although websocket stuff is designed to reconnect, it is not tested well
 - lots of missing test coverage on the API interaction side
 - TeamCity urls are hard coded in bot.py
 - only build status is reported into Slack today, and it is unformatted

Set up development env with:

``` bash
virtualenv VENV
source ./VENV/bin/activate
pip install -r requirements.txt
```

Install:
--------

```
python setup.py install
```

Requirements:
-------------

```setup.py``` should should take care of the Python code, but you need a TeamCity server and a bot API token from Slack.  I am not going to cover how to get those going since there are great docs out there.  You need to tell the bot about them, see next section:

Configuration:
--------------

 - ```~/.slackbottoken``` should contain a single line witn your Slack API token.
 - ```~/.teamcityconfig.json``` should contain something like this:

```js
{'user': 'teamcity_user_name',
 'pass': 'teamcity_user_pass'}
 ```
