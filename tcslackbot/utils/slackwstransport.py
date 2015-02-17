""" confirm we can talk web sockets to slack """

from __future__ import print_function
import urllib
import json

from twisted.internet import defer, ssl
from twisted.web import client
from autobahn.twisted.websocket import (
    WebSocketClientProtocol, WebSocketClientFactory, connectWS)


class WebSocket(WebSocketClientProtocol):

    def __init__(self, on_msg, on_lost):
        """ required to pass in some callbacks
            on_msg is called when a message comes in
            on_lost is called when the connection is lost """
        self.on_msg = on_msg
        self.on_lost = on_lost

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        self.on_msg(payload)

    def connectionLost(self, reason):
        WebSocketClientProtocol.connectionLost(self, reason)
        self.on_lost(reason)


class ClientFactory(WebSocketClientFactory):

    def __init__(self, url, on_msg, on_lost):
        WebSocketClientFactory.__init__(self, url)
        self.on_msg = on_msg
        self.on_lost = on_lost

    def buildProtocol(self, addr):
        p = self.protocol(self.on_msg, self.on_lost)
        p.factory = self
        return p


class SlackWebSocketManager(object):
    """ get the URL for connection and try to keep us connected as much as
        possible """

    def __init__(self, token):
        self.token = token
        self.factory = None

    @defer.inlineCallbacks
    def connect(self):
        ws_url = yield self._get_url()
        self.factory = \
            ClientFactory(ws_url, lambda _m: print(_m), self.on_lost)
        self.factory.protocol = WebSocket
        if self.factory.isSecure:
            contextFactory = ssl.ClientContextFactory()
        else:
            contextFactory = None
        yield connectWS(self.factory, contextFactory)

    @defer.inlineCallbacks
    def on_lost(self, reason):
        print("Lost connection {!r}".format(reason))
        self.connect()

    @defer.inlineCallbacks
    def _get_url(self):
        """ talk to the Slack API to get the WS URL,
            TODO error handling """
        url = 'https://slack.com/api/rtm.start'
        params = urllib.urlencode({'token': self.token})
        resp = yield client.getPage('{}?{}'.format(url, params))
        defer.returnValue(json.loads(resp)['url'])
        return
