
from twisted.internet import reactor
from optparse import OptionParser
from twisted.spread import pb

def execute_task():

    p = OptionParser("useage: %prog [options] TASK [args]")
    p.add_option("-h", "--hostname", description="Hostname to connect to")
    p.add_option("-p", "--port", default=pb.portno, description="Port to connect to")
    p.add_option("-u", "--username", default="guest", description="Authentication username")
    p.add_option("-P", "--password", default="guest", description="Password")
    options, args = p.parse_args()

    def success(message):
        print "Task '%s' finished executing", message
        reactor.stop()

    def failure(error):
        t = error.trap(DefinedError)
        print "error received:", t
        reactor.stop()

    def connected(perspective):
        perspective.callRemote('executeTask', args).addCallbacks(success, failure)
        print "connected."

    factory = pb.PBClientFactory()
    reactor.connectTCP(options.hostname, options.port, factory)
    factory.login(
        UsernamePassword(options.username, options.password)).addCallbacks(connected, failure)

    reactor.run()
