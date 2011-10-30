Hacking
=======

Writing custom tasks
--------------------

You can write custom tasks for Boiler to orchestrate.

First of all you subclass the :py:ref:`yaybu.boiler.task.Task` base class.
There are a few key methods you need to implement.

Here is ``mypingtask/__init__.py`` - a pointless task that pings a host::

    from twisted.internet.protocol import ProcessProtocol
    from yaybu.boiler.task import Task
    import os

    class PingProtocol(ProcessProtocol):

        def __init__(self, task):
            self.task = task

        def outReceived(self, data):
            print 'STDOUT:', data

        def errReceived(self, data):
            print 'STDERR:', data

        def connectionMade(self):
            print 'Started running subprocess'

        def processEnded(self, reason):
            print 'Completed running subprocess'

    class Ping(Task):
        def (self, target):
            self.target = target

        def start(self):
            reactor.spawnProcess(PingProtocol(self), 'ping', ['ping', self.target, '-c', 4], env=os.environ)

        def stop(self):
            pass

        def abort(self):
            pass

When Ping is defined it will be automatically registered with a factory so that
Ping tasks can be created from Yay.

Your task shouldn't start doing any work until ``start()`` is called.

In order for Boiler to find this task we need to make sure Boiler know to
import it. We do this with entry points. You need a setup.py something like
this::

    from setuptools import setup, find_packages

    setup(name='mypingtask',
      version='0.0.0',
      packages=find_packages(exclude=['ez_setup']),
      entry_points = {
        "boiler.task": ["tasks = mypingtask"],
        }
      )

