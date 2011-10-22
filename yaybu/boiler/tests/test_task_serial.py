from twisted.trial.unittest import TestCase
from twisted.internet import defer

from yaybu.boiler.task import SerialTask


class _TestTask(object):
    def __init__(self, work, *args, **kwargs):
        self.work = work
        self.args = args
        self.kwargs = kwargs

        self.deferred = defer.Deferred()

    def whenDone(self):
        return self.deferred

    def start(self):
        self.work(*self.args, **self.kwargs)
        self.deferred.callback(True)


class TestSerialTask(TestCase):

    @defer.inlineCallbacks
    def test_execute(self):
        output = []

        s = SerialTask()
        s.add(_TestTask(output.append, 1))
        s.add(_TestTask(output.append, 2))
        s.add(_TestTask(output.append, 3))
        s.start()

        yield s.whenDone()

        self.failUnlessEqual(output, [1,2,3])

