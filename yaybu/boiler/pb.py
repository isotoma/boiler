from optparse import OptionParser

from zope.interface import implements

from twisted.spread import pb
from twisted.cred.portal import IRealm, Portal
from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse
from twisted.internet import reactor
from twisted.cred.credentials import UsernamePassword

import yay

class PbPerspective(pb.Avatar):

    def perspective_execute(self, yayfile):
        d = yay.load(yayfile)
        for task in d['tasks']:
            assert len(task.keys()) == 1
            typename, instances = resource.items()[0]
            if not isinstance(instances, list):
                instances = [instances]
            for instance in instances:
                self.create(typename, instance)

    def create(self, typename, instance):
        # TODO
        pass

    def logout(self):
        pass


class PbRealm:
    implements(IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        if pb.IPerspective in interfaces:
            avatar = PbPerspective()
            return pb.IPerspective, avatar, avatar.logout
        raise NotImplementedError("no interface")


