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

from twisted.internet import defer
from twisted.python import log


class EventDescriptor(object):

    """
    This is a descriptor for attaching an Event object to a class. You attach
    it to a class like this::

        class Frobulator:
            something_happened = EventDescriptor("something_happened")

    When something_happened is accessedd a proxy object for managing listeners
    and firing events is returned.

    You can attach a listener like this::

        f = Frobulator()
        f.something_happened.listen(my_callback)

    You can fire an event like this::

        f.fire(foo=1, bar=2, baz=3)

    The ``fire`` method returns a deferred object that you can use to pause
    execution of your code until all callbacks have finished. This is optional,
    of course.
    """

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if not instance:
            raise AttributeError

        callbacks = instance.__dict__.setdefault("__event_%s" % self.name, [])
        return Event(callbacks)


class Event(object):

    """
    Manage listening to and firing events
    """

    def __init__(self, callbacks):
        self.callbacks = callbacks

    def listen(self, callback):
        self.callbacks.append(callback)

    def fire(self, **kwargs):
        """
        Trigger an event - call all the callbacks attached to it.

        The callbacks may optionally return deferreds.

        When an event is fired a ``DeferredList`` is returned which can be
        optionally used to pause execution until all callbacks have finished.

        If a callback raises an error we capture and log it and move on to the
        next callback.
        """
        deferreds = []
        for callback in self.callbacks:
            try:
                d = defer.maybeDeferred(callback, **kwargs)
                deferreds.append(d)
            except:
                log.err()
        return defer.DeferredList(deferreds)

