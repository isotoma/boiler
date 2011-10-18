
import os

from twisted.application import service, internet
from twisted.spread import pb
from twisted.cred.portal import Portal
from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse

from yaybuserver.pb import PbRealm

port = int(os.environ["YAYBU_SERVER_PORT"])

application = service.Application("Yaybu Server")

portal = Portal(PbRealm())

checker = InMemoryUsernamePasswordDatabaseDontUse()
checker.addUser("guest", "guest")
portal.registerChecker(checker)

service = internet.TCPServer(port, pb.PBServerFactory(portal))
service.setServiceParent(application)
