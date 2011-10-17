from twisted.internet import defer


class Interrupted(Failure):
    """
    An exception that is raised when a Task is interrupted
    """
    pass


class Task(object):

    """
    A base class for an interruptible, asynchronous piece of work.
    """

    def __init__(self):
        self.deferred = defer.Deferred()

    def whenDone(self):
        """
        Returns a deferred that is fired when a task is completed, or when a
        task has failed
        """
        return self.deferred

    def start(self):
        """
        Actually execute a task. This only starts a task.
        """
        pass

    def stop(self):
        """
        Stop this task safely
        """
        return defer.succeed()

    def abort(self):
        """
        Stop this task immediately and aggressively
        """
        return defer.succeed()


class Tasks(Service):

    """
    Manages any tasks that are in progress

    We could potentially rate limit this in the future
    """

    def __init__(self):
        Service.__init__(self)
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

