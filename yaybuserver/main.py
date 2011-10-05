from twisted.application import service
from twisted.python import usage


class Options(usage.Options):
    optParameters = [
        ["config", "c", "yaybu-server.yay", "Configuration file"],
        ]


def makeService(config):
    s = service.MultiService()

    return s


