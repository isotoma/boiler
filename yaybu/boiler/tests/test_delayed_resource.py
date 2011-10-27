from mock import Mock

from twisted.internet import defer
from twisted.trial.unittest import TestCase

from yaybu.boiler.services.web import DelayedResource


class TestDelayedResource(TestCase):

    def test_non_deferred_response(self):
        class X(DelayedResource):
            def handle(self, req):
                return "done"

        request = Mock()
        X().render(request)
        request.write.assert_called_with("done")

    def test_deferred_ok_response(self):
        d = defer.Deferred()
        class X(DelayedResource):
            def handle(self, req):
                return d

        request = Mock()
        X().render(request)
        d.callback("done")
        request.write.assert_called_with("done")

    def test_fail_response(self):
        class X(DelayedResource):
            def handle(self, req):
                raise RuntimeError("A fake error has occured")

        request = Mock()
        X().render(request)
        assert request.processingFailed.called

