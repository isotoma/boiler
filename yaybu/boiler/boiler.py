
from twisted.application.service import MultiService

import yay
from yaybu.boiler.task import Tasks, ParallelTask, TaskType


class Boiler(MultiService):

    """
    Orchestrate multiple deployments
    """

    def __init__(self, config=None):
        MultiService.__init__(self)
        self.config = config

        # Create a tasks queue
        self.tasks = Tasks()
        self.tasks.setServiceParent(self)

    def execute_yay(self, stream):
        """
        Takes a stream containing tasks encoded as Yay and executes them.

        Returns an object implementing ITask for tracking execution of
        the tasks.
        """
        d = yay.load(stream)
        p = ParallelTask(TaskType.create_all(d['tasks'])
        self.tasks.add(p)
        return p


