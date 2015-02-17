""" confirm we can talk web sockets to slack """

from __future__ import print_function
import urllib
import json

from twisted.internet import defer, ssl, reactor
from twisted.web import client
from autobahn.twisted.websocket import (
    WebSocketClientProtocol, WebSocketClientFactory, connectWS)


CONNECT_DELAY = 5  # TODO make this a backoff timer


class WebSocket(WebSocketClientProtocol):

    def __init__(self, on_msg, on_lost, on_connnect):
        """ required to pass in some callbacks
            on_msg is called when a message comes in
            on_lost is called when the connection is lost """
        self.on_msg = on_msg
        self.on_lost = on_lost

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))
        self.on_connect(response)

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        self.on_msg(payload)

    def connectionLost(self, reason):
        WebSocketClientProtocol.connectionLost(self, reason)
        self.on_lost(reason)


class ClientFactory(WebSocketClientFactory):

    def __init__(self, url, on_msg, on_lost, on_connect):
        WebSocketClientFactory.__init__(self, url)
        self.on_msg = on_msg
        self.on_lost = on_lost
        self.on_connect = on_connect

    def buildProtocol(self, addr):
        p = self.protocol(self.on_msg, self.on_lost, self.on_connect)
        p.factory = self
        return p


class SlackWebSocketManager(object):
    """ get the URL for connection and try to keep us connected as much as
        possible """

    def __init__(self, token, on_msg):
        self.token = token
        self.on_msg = on_msg
        self.factory = None

    @defer.inlineCallbacks
    def connect(self):
        ws_url = yield self._get_url()
        self.factory = \
            ClientFactory(ws_url, self.on_msg, self.on_lost, self.on_connect)
        self.factory.protocol = WebSocket
        if self.factory.isSecure:
            contextFactory = ssl.ClientContextFactory()
        else:
            contextFactory = None
        result = yield connectWS(self.factory, contextFactory)
        print(result)

    def on_lost(self, reason):
        print("Lost connection {!r}".format(reason))
        reactor.callLater(CONNECT_DELAY,  self.connect)

    def on_connect(self, response):
        import pdb; pdb.set_trace()
        print(response)

    @defer.inlineCallbacks
    def _get_url(self):
        """ talk to the Slack API to get the WS URL,
            TODO error handling """
        url = 'https://slack.com/api/rtm.start'
        params = urllib.urlencode({'token': self.token})
        resp = yield client.getPage('{}?{}'.format(url, params))
        defer.returnValue(json.loads(resp)['url'])
        return
