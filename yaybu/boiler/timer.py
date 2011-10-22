
from twisted.application.internet import TimerService


class TimedDeployment(TimerService):
    """
    Queues a deployment every 5 minutes, but only when the previous one has finished.
    """

    def __init__(self, step=5*60):
        TimerService.__init__(step, self.fire)

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

