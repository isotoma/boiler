
from twisted.application.service import MultiService

import yay
from yaybu.boiler.task import Tasks, ParallelTask


class Boiler(MultiService):

    """
    Orchestrate multiple deployments
    """

    def __init__(self, config):
        self.config = config

        # Create a tasks queue
        self.tasks = Tasks()
        self.tasks.setServiceParent(self)

    def execute_yay(self, yay):
        """
        Takes a stream containing tasks encoded as Yay and executes them.

        Returns an object implementing ITask for tracking execution of
        the tasks.
        """
        d = yay.load(yay)
        p = ParallelTask()
        for task in d['tasks']:
            assert len(task.keys()) == 1
            typename, instances = task.items()[0]
            if not isinstance(instances, list):
                instances = [instances]
            for instance in instances:
                t = self.create(typename, instance)
                p.add(t)
        self.tasks.add(p)
        return p

    def create(self, typename, instance):
        # TODO
        pass


