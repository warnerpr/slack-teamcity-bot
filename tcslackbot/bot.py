from __future__ import print_function

import json
from twisted.internet import reactor, defer
from tcslackbot.utils import slacktoken
from tcslackbot.utils import slackwstransport


import re
# TODO put this into a data file / DB
PATT = \
    r'(?P<base>http://localhost:8111/)(viewLog.html\?)' \
    '(buildId=)(?P<build_id>\d+)'
TC_LINK_PATT = re.compile(PATT)
TC_LINK_FORMAT = '{base}httpAuth/app/rest/builds/id:{build_id}'


class TcSlackBot(object):

    @defer.inlineCallbacks
    def on_message(self, msg):
        data = json.loads(msg)
        if data.get('type', None) == 'message':
            for url in look_for_urls(data['text']):
                yield self.summarize(url, data["channel"])

    @defer.inlineCallbacks
    def summarize(self, url, channel):
        import xml.etree.ElementTree as ET
        from treq import get
        resp = yield get(url, auth=('admin', 'adminpw'))
        page = yield resp.content()
        print(page)
        root = ET.fromstring(page)
        status = root.get('status')
        self.wsman.ws.sendMessage(json.dumps(
            {"type": "message", "text": status, "channel": channel}))
        return


def look_for_urls(msg):
    """
    look for TeamCity GUI links and convert them into API links, find all of
    them in msg
    look for something like:
       'http://localhost:8111/viewLog.html?buildId=4&
        buildTypeId=TcSlackBotTests_Test&tab=buildResultsDiv'
     and yield
        'http://localhost:8111/httpAuth/app/rest/builds/id:4'
    """
    print (msg)
    for match in re.finditer(TC_LINK_PATT, msg):
        url = TC_LINK_FORMAT.format(**match.groupdict())
        print (url)
        yield url


def main():
    token = slacktoken.get_token()
    bot = TcSlackBot()
    wsman = slackwstransport.SlackWebSocketManager(token, bot.on_message)
    bot.wsman = wsman
    reactor.callWhenRunning(wsman.connect)
    reactor.run()


if __name__ == '__main__':
    main()
