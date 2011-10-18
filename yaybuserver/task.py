from twisted.internet import defer

# Need to think carefully about behaviour when failing and interrupted vs success

class Interrupted(Failure):
    """
    An exception that is raised when a Task is interrupted
    """
    pass


class Task(object):

    """
    Actions performed by Yaybu Server are modelled as a Task. The act of
    deploying with Yaybu is decoupled from the Task management code to
    allow other tasks to be orchestrated by Yaybu.
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


class CompoundTask(Task):

    """
    A set of tasks that should be performed in sequence.

    Perhaps you use Fabric to poke Nagios on a second server after deploying to the first.
    """

    def __init__(self, *tasks):
        super(Task, self).__init__()
        self.tasks = tasks
        self.current = None

    def addTask(self, task):
        self.tasks.append(task)

    def startNext(self):
        """ Get the next task and start it. That task is set to call back when it is finished. """
        if not self.tasks:
            return
        self.current = t = self.tasks[0]
        del self.tasks[0]
        t.whenDone().addCallback(self.startNext)
        t.start()

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


class Tasks(Service):

    """
    Manages any tasks that are in progress

    Currently any queued tasks are started immediately. A list of active
    tasks is kept so we can stop or abort them during a shutdown.

    We could potentially rate limit this in the future by putting incoming
    tasks into a queue list.
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

