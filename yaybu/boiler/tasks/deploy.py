# Copyright 2011 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from twisted.conch.ssh import transport, userauth, connection, common, keys, channel
from twisted.internet import defer, protocol, reactor
from twisted.python import log
import struct, sys, getpass, os

from twisted.web.http import HTTPChannel, Request

from yaybu.boiler.task import Task


class YaybuTransport(transport.SSHClientTransport):

    def __init__(self, username, yay):
        transport.SSHClientTransport.__init__(username)
        self.username = username
        self.yay = yay

    def verifyHostKey(self, hostKey, fingerprint):
        print 'host key fingerprint: %s' % fingerprint
        return defer.succeed(1)

    def connectionSecure(self):
        self.requestService(
            YaybuAuthenticator(self.username,
                YaybuConnection(self.yay)))

    def getPeer(self):
        return ('', )

    def getHost(self):
        return ('', )


class YaybuAuthenticator(userauth.SSHUserAuthClient):

    """
    A service implementing the client side of "ssh-userauth"

    The bulk of this is already provided by ``twisted.conch.ssh.userauth.SSHUserAuthClient``,
    we just plumb SSH key retrieval in to conch.
    """

    def getPassword(self):
        """
        We explicitly do not support interactive password logins or storing passwords to other servers
        """
        return defer.fail(NotImplementedError())

    def getGenericAnswers(self, name, instruction, questions):
        """
        Not implemented as this service is non-interactive
        """
        return defer.fail(NotImplementedError())

    def getPublicKey(self):
        path = os.path.expanduser('~/.ssh/id_dsa')
        # this works with rsa too
        # just change the name here and in getPrivateKey
        if not os.path.exists(path) or self.lastPublicKey:
            # the file doesn't exist, or we've tried a public key
            return
        return keys.Key.fromFile(filename=path+'.pub').blob()

    def getPrivateKey(self):
        path = os.path.expanduser('~/.ssh/id_dsa')
        return defer.succeed(keys.Key.fromFile(path).keyObject)


class YaybuConnection(connection.SSHConnection):

    """
    A session representing a connection to a target server.

    Establishes the Yaybu communication channel and SSH credential forwarding.
    """

    def __init__(self, stream):
        self.stream = stream
        connection.SSHConnection.__init__()

    def serviceStarted(self):
        self.openChannel(YaybuChannel(self.stream))


class YaybuRequest(Request):

    """
    A custom request that responds to HTTP-over-SSH requests
    """

    def __init__(self, *a, **kw):
        self.yay = kw.pop('yay')
        Request.__init__(self, *a, **kw)


    def four_oh_four(self):
        self.setResponseCode(404)
        self.setHeader("Content-Type", "application/octect-stream")
        self.setHeader('Connection', 'close')#keep-alive')
        self.setHeader('Content-Length', '0')
        self.finish()

    def process_config(self):
        import pickle
        body = pickle.dumps(self.yay)

        self.setResponseCode(200)
        self.setHeader("Content-Type", "application/octect-stream")
        self.setHeader('Content-Length', str(len(body)))
        self.setHeader('Connection', 'close') #keep-alive')
        self.write(body)
        self.finish()

    def process_changelog(self):
        body = self.content.read()
        log.msg(body)

        self.setResponseCode(200)
        self.setHeader("Content-Type", "application/octet-stream")
        self.setHeader("Content-Length", "0")
        self.setHeader("Connection", 'close')#keep-alive')
        self.write('')
        self.finish()

    def process(self):
        log.msg(self.clientproto)
        log.msg(self.getAllHeaders())

        if not self.path.startswith("/"):
            self.four_oh_four()
            return

        path = self.path[1:]

        if path.endswith("/"):
            path = path[:-1]

        if "/" in path:
            self.four_oh_four()
            return

        print path

        if hasattr(self, "process_" + path):
            getattr(self, "process_" + path)()
            return

        self.four_oh_four()


class YaybuChannel(channel.SSHChannel):

    name = 'session'

    def __init__(self, yay):
        channel.SSHChannel.__init__(self)
        self.protocol = HTTPChannel()
        self.protocol.requestFactory = self.request_factory
        self.protocol.transport = self
        self.disconnecting = False
        self.yay = yay

    def request_factory(self):
        return YaybuRequest(self.yay)

    def openFailed(self, reason):
        print 'echo failed', reason

    def channelOpen(self, ignoredData):
        self.data = ''
        d = self.conn.sendRequest(self, 'exec', common.NS('yaybu --remote -'), wantReply = 1)
        #d.addCallback(self._cbRequest)

    def _cbRequest(self, ignored):
        #self.write('hello conch\n')
        #self.conn.sendEOF(self)
        pass

    def dataReceived(self, data):
        self.protocol.dataReceived(data)

    def closed(self):
        self.loseConnection()
        reactor.stop()


class YaybuTask(Task):

    """
    Provides an interruptable task that actually does a deployment
    """

    def __init__(self, host, yay, username='root', port=22):
        self.host = host
        self.username = username
        self.port = 22
        self.protocol = None
        self.yay = yay
        self.deferred = defer.Deferred()

    @defer.inlineCallbacks
    def start(self):
        self.protocol = yield protocol.ClientCreator(reactor, YaybuTransport(self.username)).connectTCP(self.host, self.port)

    def stop(self):
        #FIXME: Investigate safer ways to do this, probably need Yaybu to respect signals so we can 'stop after current step' or something
        #FIXME: Does task API need a graceful stop and a forced stop?
        self.protocol.transport.loseConnection()

