
from twisted.application.internet import TimerService
from yaybu.boiler.service import BoilerService

class TimedDeployment(BoilerService):
    """
    Queues a deployment every 5 minutes, but only when the previous one has finished.
    """

    def __init__(self, step=5*60):
        BoilerService.__init__(self)
        TimerService(step, self.fire).setServiceParent(self)

    def fire(self):
        """ I am called every 5 minutes by TimerService and run some Yay """

        t = self.parent.execute_yay("""
            host: localhost
            port: 22
            config:
                resources:
                  - File:
                      name: /tmp/foo
            """)

        return t.whenDone()

