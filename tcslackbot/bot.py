from __future__ import print_function


from twisted.internet import reactor
from tcslackbot.utils import slacktoken
from tcslackbot.utils import slackwstransport

class Echoer(object):
    def echo(self, msg):
        import json
        data = json.loads(msg)
        if data.get('type', None) == 'message':
            self.wsman.ws.sendMessage(json.dumps(
                {"type": "message", "text": "echo eco eco", "channel": data["channel"]}))

def main():
    token = slacktoken.get_token()
    echoer = Echoer()
    wsman = slackwstransport.SlackWebSocketManager(token, echoer.echo)
    echoer.wsman = wsman
    reactor.callWhenRunning(wsman.connect)
    reactor.run()


if __name__ == '__main__':
    main()

