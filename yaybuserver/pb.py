from optparse import OptionParser

from zope.interface import implements

from twisted.spread import pb
from twisted.cred.portal import IRealm, Portal
from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse
from twisted.internet import reactor
from twisted.cred.credentials import UsernamePassword

class DefinedError(pb.Error):
    pass


class PbPerspective(pb.Avatar):

    def perspective_echo(self, text):
        print 'echoing',text
        return text

    def perspective_error(self):
        raise DefinedError("exception!")

    def logout(self):
        print self, "logged out"


class PbRealm:
    implements(IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        if pb.IPerspective in interfaces:
            avatar = PbPerspective()
            return pb.IPerspective, avatar, avatar.logout 
        raise NotImplementedError("no interface")


def main_server():
    portal = Portal(PbRealm())

    checker = InMemoryUsernamePasswordDatabaseDontUse()
    checker.addUser("guest", "guest")
    portal.registerChecker(checker)

    reactor.listenTCP(pb.portno, pb.PBServerFactory(portal))
    reactor.run()


def execute_task():
    """
    An entry point for a simple task executor that runs from the command line

    Useful for deploying from, for example, a git pre-receive hook.
    """
    p = OptionParser("useage: %prog [options] TASK")
    p.add_option("-s", "--stdout", description="Output log information to stdout")
    p.add_option("-u", "--unix-socket", description="A unix socket to connect to")
    options, args = p.parse_args()

    def success(message):
        print "Task '%s' finished executing", message
        reactor.stop()

    def failure(error):
        t = error.trap(DefinedError)
        print "error received:", t
        reactor.stop()

    def connected(perspective):
        perspective.callRemote('executeTask', args[0]).addCallbacks(success, failure)
        print "connected."

    factory = pb.PBClientFactory()
    reactor.connectTCP("localhost", pb.portno, factory)
    factory.login(
        UsernamePassword("guest", "guest")).addCallbacks(connected, failure)

    reactor.run()


