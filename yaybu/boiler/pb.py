from optparse import OptionParser

from zope.interface import implements

from twisted.spread import pb
from twisted.cred.portal import IRealm, Portal
from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse
from twisted.internet import reactor
from twisted.cred.credentials import UsernamePassword

from yaybu.boiler.service import BoilerService


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


class PbService(BoilerService):

    def __init__(self, port=8787):
        portal = Portal(PbRealm(boiler))

        checker = InMemoryUsernamePasswordDatabaseDontUse()
        checker.addUser("guest", "guest")
        portal.registerChecker(checker)

        service = strports.service(port, pb.PBServerFactory(portal))
        service.setServiceParent(self)

