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

from optparse import OptionParser

from zope.interface import implements

from twisted.spread import pb
from twisted.cred.portal import IRealm, Portal
from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse
from twisted.internet import reactor
from twisted.cred.credentials import UsernamePassword
from twisted.application import strports

from yaybu.boiler.service import BaseService


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


class PbService(BaseService):

    def __init__(self, port=8787):
        BaseService.__init__(self)

        boiler = None
        portal = Portal(PbRealm(boiler))

        checker = InMemoryUsernamePasswordDatabaseDontUse()
        checker.addUser("guest", "guest")
        portal.registerChecker(checker)

        service = strports.service("tcp:%d" % port, pb.PBServerFactory(portal))
        service.setServiceParent(self)

