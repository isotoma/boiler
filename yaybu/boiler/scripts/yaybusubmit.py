
import sys

from twisted.internet import reactor
from optparse import OptionParser
from twisted.spread import pb
from twisted.cred.credentials import UsernamePassword

def run():

    p = OptionParser("%prog [options] [filename]")
    p.add_option("-H", "--hostname", default="localhost", help="Hostname to connect to")
    p.add_option("-p", "--port", default=pb.portno, help="Port to connect to")
    p.add_option("-u", "--username", default="guest", help="Authentication username")
    p.add_option("-P", "--password", default="guest", help="Password")
    options, args = p.parse_args()

    if len(args) == 0:
        stream = sys.stdin
    elif len(args) == 1:
        stream = open(args[0])
    else:
        p.print_usage()
        raise SystemExit

    task = stream.read()

    def success(message):
        print "Task '%s' finished executing" % message
        reactor.stop()

    def failure(error):
        #t = error.trap(DefinedError)
        print "error received:", error
        reactor.stop()

    def connected(perspective):
        perspective.callRemote('execute', task).addCallbacks(success, failure)
        print "connected."

    factory = pb.PBClientFactory()
    reactor.connectTCP(options.hostname, options.port, factory)
    factory.login(
        UsernamePassword(options.username, options.password)).addCallbacks(connected, failure)

    reactor.run()

