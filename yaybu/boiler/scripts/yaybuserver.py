from __future__ import absolute_import

import sys
import os

from twisted.python import usage
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


class YaybuServerOptions(ServerOptions):

    @property
    def subCommands(self):
        yield ("start", None, lambda: usage.Options(), "Start the server")
        yield ("stop", None, lambda: usage.Options(), "Stop the server")


class YaybuApplicationRunner(_SomeApplicationRunner):

    def createOrGetApplication(self):
        import os

        from twisted.application import service, internet
        from twisted.spread import pb
        from twisted.cred.portal import Portal
        from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse

        from yaybu.boiler.pb import PbRealm

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
    YaybuApplicationRunner(config).run()


def run():
    config = YaybuServerOptions()

    try:
        config.parseOptions()
    except usage.error, ue:
        print config
        print "%s: %s" % (sys.argv[0], ue)
        sys.exit(1)

    if config.subCommand == "start":
        # we pass arguments through to the tac file using the environment
        os.environ["YAYBU_SERVER_PORT"] = str(8787)
        app.run(runApp, YaybuServerOptions)

    elif config.subCommand == "stop":
        try:
            pid = int(open(pidfile).read())
        except IOError:
            print "Server is not running"
            return 255
        os.kill(pid, 15)

    else:
        usage()
        return 255

