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

from yaybu.boiler.boiler import Boiler

class YaybuServerOptions(ServerOptions):

    @property
    def subCommands(self):
        yield ("start", None, lambda: usage.Options(), "Start the server")
        yield ("stop", None, lambda: usage.Options(), "Stop the server")


class YaybuApplicationRunner(_SomeApplicationRunner):

    def createOrGetApplication(self):
        application = service.Application("Yaybu Server")

        boiler = Boiler()
        boiler.setServiceParent(application)

        config = yay.load(StringIO("""
            services:
                - PbService:
                      port: 8787
             """))

        for subservice in ServiceType.create_all(config.get("services", [])):
            subservice.setServiceParent(boiler)

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

