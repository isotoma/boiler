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

from __future__ import absolute_import

import sys
import os

from twisted.python import usage
from twisted.python.util import sibpath

from twisted.application import app, service
from twisted.python.runtime import platformType

if platformType == "win32":
    from twisted.scripts._twistw import ServerOptions, \
    WindowsApplicationRunner as _SomeApplicationRunner
else:
    from twisted.scripts._twistd_unix import ServerOptions, \
    UnixApplicationRunner as _SomeApplicationRunner

import yay, StringIO
from yaybu.boiler.boiler import Boiler
from yaybu.boiler.service import ServiceType
import yaybu.boiler.services


class StartOptions(ServerOptions):

    """
    Options for starting a boiler daemon.

    Subclasses ServerOptions from twistd - either a Unix or Win32 version.
    """

    longdesc = "Start the service"

    @property
    def subCommands(self):
        # There are no subcommands for start - but twistd uses a hasattr check
        # so we have to raise an AttributeError to trick it
        raise AttributeError

    @property
    def synopsis(self):
        # Need to undo the fact that ServerOptions overrides the default synopsis
        # as it stops us nesting the ServerOptions
        raise AttributeError


class StopOptions(usage.Options):

    longdesc = "Stop the service"


class Options(usage.Options):
    subCommands = [
        ['start', None, StartOptions, "Start the service"],
        ['stop', None, StopOptions, "Stop the service"],
        ]

    optParameters = [
        ['config', 'c', '/etc/yaybu-boiler', 'Server configuration file'],
        ]

    def postOptions(self):
        if not "config" in self:
            raise usage.UsageError("No configuration file provided")

        if not os.path.exists(self['config']):
            raise usage.UsageError("The configuration file '%s' does not exist" % self['config'])


class YaybuApplicationRunner(_SomeApplicationRunner):

    def createOrGetApplication(self):
        application = service.Application("Yaybu Server")

        boiler = Boiler()
        boiler.setServiceParent(application)

        config = yay.load_uri(self.config.parent["config"])

        for subservice in ServiceType.create_all(config.get("services", [])):
            subservice.setServiceParent(boiler)

        return application


def run():
    config = Options()

    try:
        config.parseOptions()
    except usage.error, ue:
        print "Error: %s" % ue
        print config.opt_help()
        sys.exit(1)

    if config.subCommand == "start":
        YaybuApplicationRunner(config.subOptions).run()

    elif config.subCommand == "stop":
        try:
            pid = int(open(pidfile).read())
        except IOError:
            print "Server is not running"
            return 255
        os.kill(pid, 15)

    else:
        config.opt_help()
        sys.exit(1)

