from __future__ import absolute_import

import sys
import os

from twisted.python.util import sibpath
from twisted.spread import pb

from twisted.application import app
from twisted.python.runtime import platformType

if platformType == "win32":
    from twisted.scripts._twistw import ServerOptions, \
    WindowsApplicationRunner as _SomeApplicationRunner
else:
    from twisted.scripts._twistd_unix import ServerOptions, \
    UnixApplicationRunner as _SomeApplicationRunner


class YaybuApplicationRunner(_SomeApplicationRunner):

    def createOrGetApplication(self):
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

        return application


def runApp(config):
    _SomeApplicationRunner(config).run()


def usage():
    print >>sys.stderr, "Usage: yaybuserver stop | start"

def run(pidfile, logfile, port=pb.portno):
    if len(sys.argv) != 2:
        usage()
        return 255

    command = sys.argv[1]

    if command == "start":
        # we pass arguments through to the tac file using the environment
        os.environ["YAYBU_SERVER_PORT"] = str(port)
        app.run(runApp, ServerOptions)

    elif command == "stop":
        try:
            pid = int(open(pidfile).read())
        except IOError:
            print "Server is not running"
            return 255
        os.kill(pid, 15)

    else:
        usage()
        return 255

