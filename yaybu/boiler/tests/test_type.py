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

