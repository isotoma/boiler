
from zope.interface import Interface

class ITask(Interface):

    """
    Actions performed by Yaybu Server are modelled as a Task. The act of
    deploying with Yaybu is decoupled from the Task management code to
    allow other tasks to be orchestrated by Yaybu.
    """

    def whenDone():
        """
        Returns a deferred that is fired when a task is completed, or when a
        task has failed
        """

    def start():
        """
        Actually execute a task. This only starts a task.
        """

    def stop():
        """
        Stop this task safely
        """

    def abort():
        """
        Stop this task immediately and aggressively
        """

