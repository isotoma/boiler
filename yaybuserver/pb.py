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


