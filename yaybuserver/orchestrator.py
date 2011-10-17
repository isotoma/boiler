
from twisted.application.service import MultiService

from yaybuserver.task import Tasks


class Orchestrator(MultiService):

    """
    Orchestrate multiple deployments
    """

    def __init__(self, config):
        self.config = config

        # Create a tasks queue
        self.tasks = Tasks()
        self.tasks.setServiceParent(self)

    def startService(self):
        # Iterate over a list of nodes or servers and do deployments

