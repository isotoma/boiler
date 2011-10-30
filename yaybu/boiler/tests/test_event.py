from twisted.internet import defer
from twisted.trial.unittest import TestCase

from yaybu.boiler.events import EventDescriptor


class Frobulator(object):
    something_happened = EventDescriptor("something_happened")
    """ Doc strings can go here and be picked up by sphinx """

    def do_something(self):
        return self.something_happened.fire()


class TestEvent(TestCase):

    def test_listen(self):
        def _():
            pass

        f = Frobulator()
        f.something_happened.listen(_)
        self.failUnlessEqual(f.something_happened.callbacks, [_])

    def test_multiple_listen(self):
        def _():
            pass

        f, g = Frobulator(), Frobulator()
        f.something_happened.listen(_)
        g.something_happened.listen(_)
        g.something_happened.listen(_)

        self.failUnlessEqual(len(f.something_happened.callbacks), 1)
        self.failUnlessEqual(len(g.something_happened.callbacks), 2)

    def test_callback_deferreds(self):
        """ Test that the Deferred returned by an event firing does indeed
        wait until all callbacks have finished before it fires """
        d = defer.Deferred()
        e = defer.Deferred()

        f = Frobulator()
        f.something_happened.listen(lambda: d)
        f.something_happened.listen(lambda: e)

        order = []

        cb = f.something_happened.fire()
        cb.addCallback(lambda x: order.append(3))

        order.append(1)
        d.callback(1)

        order.append(2)
        e.callback(2)

        # If the order is 1,2,3 we know both deferreds were fired before
        # the Event.fire() deferred fired.
        self.failUnlessEqual(order, [1,2,3])


