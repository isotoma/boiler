

class Task(object):

    def __init__(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass


class Tasks(Service):

    """
    Manages any tasks that are in progress

    We could potentially rate limit this in the future
    """

    def add(self, task):
        pass

    def stopService(self):
        """
        Aborts again in-flight deployments or wait for them to finish?
        """


