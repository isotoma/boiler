
from twisted.application.internet import TimerService


class TimedDeployment(TimerService):
    """
    Queues a deployment every 5 minutes, but only when the previous one has finished.
    """

    def __init__(self, step=5*60):
        TimerService.__init__(step, self.fire)

    def fire(self):
        t = DeployTask("localhost")
        self.parent.queueTask(t)
        return t.whenDone()

