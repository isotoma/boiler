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

from zope.interface import implements

from twisted.internet import defer
from twisted.application import service

from yaybu.boiler.iyaybuserver import ITask
from yaybu.boiler.type import Instanceable

# Need to think carefully about behaviour when failing and interrupted vs success

class Interrupted(BaseException):
    """
    An exception that is raised when a Task is interrupted
    """
    pass


class TaskType(Instanceable):
    pass


class Task(object):
    __metaclass__ = TaskType


class SerialTask(Task):

    """
    A set of tasks that should be performed in sequence.

    Perhaps you use Fabric to poke Nagios on a second server after deploying to the first.
    """

    implements(ITask)

    def __init__(self, *tasks):
        self.tasks = list(tasks)
        self.current = None
        self.deferred = defer.Deferred()

    def add(self, task):
        self.tasks.append(task)

    def startNext(self, val=None):
        """ Get the next task and start it. That task is set to call back when it is finished. """
        if not self.tasks:
            self.deferred.callback(True)
            return
        self.current = t = self.tasks[0]
        del self.tasks[0]
        t.whenDone().addCallback(self.startNext)
        t.start()

    def whenDone(self):
        return self.deferred

    def start(self):
        self.startNext()

    def stop(self):
        """ Clears any remaining subtasks and stops the current one """
        self.tasks = []
        return self.current.stop()

    def abort(self):
        """ Clears any remaining subtasks and aborts the current one """
        self.tasks = []
        return self.current.abort()


class ParallelTask(Task):

    """
    A set of tasks that can be executed in parallel
    """

    implements(ITask)

    def __init__(self, *tasks):
        self.tasks = list(tasks)
        self.current = None
        self.deferred = defer.Deferred()

    def add(self, task):
        self.tasks.append(task)

    def whenDone(self):
        return self.deferred

    def start(self):
        """
        Start all tasks in this group. When all tasks have finished 
        """
        d = defer.DeferredList([t.whenDone() for t in self.tasks])
        d.addCallbacks(self.deferred.callback, self.deferred.errback)

        [t.start() for t in self.tasks]

    def stop(self):
        """
        Stop all tasks in this group and return a DeferredList that fires
        when they have all stopped.
        """
        return defer.DeferredList([t.stop() for t in self.tasks])

    def abort(self):
        """
        Abort all tasks in this group and return a DeferredList that fires
        when they have all aborted.
        """
        return defer.DeferredList([t.abort() for t in self.tasks])


class Tasks(service.Service):

    """
    Manages any tasks that are in progress

    Currently any queued tasks are started immediately. A list of active
    tasks is kept so we can stop or abort them during a shutdown.

    We could potentially rate limit this in the future by putting incoming
    tasks into a queue list.
    """

    def __init__(self):
        self.active = []

    def add(self, task):
        """
        Start tracking and executing a task
        """
        self.active.append(task)
        task.whenDone().addCallback(self.active.remove, task)
        task.start()

    def stopAllTasks(self):
        """
        Stop any active tasks this service is tracking
        """
        return defer.DeferredList(list(t.stop() for t in self.active))

    def stopService(self):
        """
        Cleanly stop this service

        Aborts again in-flight deployments or wait for them to finish?
        """
        return self.stopAllTasks()

