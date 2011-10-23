from twisted.trial.unittest import TestCase

from yaybu.boiler.type import Instanceable

class _TestType(Instanceable):
    pass

class _TestBase(object):
    __metaclass__ = _TestType

class Foo(_TestBase):
    def __init__(self, name=None):
        self.name = name

class TestType(TestCase):

    def test_create_one(self):
        freddy = _TestType.create_one("Foo", name="Freddy")
        self.failUnless(isinstance(freddy, Foo))
        self.failUnlessEqual(freddy.name, "Freddy")

    def test_create_all(self):
        freddies = _TestType.create_all([
            {"Foo": {"name": "Freddy"}},
            ])

        self.failUnless(isinstance(freddies[0], Foo))
        self.failUnlessEqual(freddies[0].name, "Freddy")

