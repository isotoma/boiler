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

from twisted.application import strports, service
from twisted.web import server, static
from twisted.web.resource import Resource
from twisted.internet import reactor, defer


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

