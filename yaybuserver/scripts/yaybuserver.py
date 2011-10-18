from __future__ import absolute_import

from twisted.scripts.twistd import run as twistd_run
from twisted.python.util import sibpath
from twisted.spread import pb
import sys
import os

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
        sys.argv[1:] = [
            '-y', sibpath(__file__, "yaybuserver.tac"),
            '--pidfile', pidfile,
            '--logfile', logfile,
        ]
        twistd_run()
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

