
from twisted.application import strports, service
from twisted.web import server, static


from yaybu.boiler.service import BaseService


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

