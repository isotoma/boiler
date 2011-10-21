from optparse import OptionParser

from zope.interface import implements

from twisted.spread import pb
from twisted.cred.portal import IRealm, Portal
from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse
from twisted.internet import reactor
from twisted.cred.credentials import UsernamePassword

import yay

class PbPerspective(pb.Avatar):

    def __init__(self, boiler):
        self.boiler = boiler

    def perspective_execute(self, yayfile):
        t = self.boiler.execute_yay(yayfile)

    def logout(self):
        pass


class PbRealm(object):

    implements(IRealm)

    def __init__(self, boiler):
        self.boiler = boiler

    def requestAvatar(self, avatarId, mind, *interfaces):
        if pb.IPerspective in interfaces:
            avatar = PbPerspective(self.boiler)
            return pb.IPerspective, avatar, avatar.logout
        raise NotImplementedError("no interface")


