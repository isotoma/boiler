
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

