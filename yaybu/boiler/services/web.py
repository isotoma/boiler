
from twisted.application import strports, service
from twisted.web import server, static
from twisted.web.resource import Resource
from twisted.internet import reactor


from yaybu.boiler.service import BaseService


class DelayedResource(Resource):

    """
    A thin shim to allow resource rendering to be more easily asynchronous

    Subclasses should implemented the ``handle`` method and may return a
    deferred.
    """

    def handle(self, request):
        raise NotImplemented(self.handle)

    def render(self, request):
        d = defer.maybeDeferred(self.handle, request)

        def _(data):
            if isinstance(data, unicode):
                data = data.encode("utf-8")
            request.write(data)
            request.finish()

        d.addCallbacks(_, request.processingFailed)

        return server.NOT_DONE_YET


class WebService(BaseService):

    """
    Simple web frontend
    """

    def __init__(self, port=8080):
        BaseService.__init__(self)

        # Create a site structure
        root = static.Data("placeholder", "text/plain")
        root.putChild("", static.Data("Index", "text/plain"))
        self.site = server.Site(root)

        # Actually service the site
        s = strports.service("tcp:%d" % port, self.site)
        s.setServiceParent(self)

