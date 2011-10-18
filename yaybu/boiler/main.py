import yay

from twisted.application import service
from twisted.python import usage

from yaybuserver.orchestartor import Orchestrator


class Options(usage.Options):
    optParameters = [
        ["config", "c", "yaybu-server.yay", "Configuration file"],
        ]


def makeService(config):
    config = yay.load_uri(config['config'])
    return Orchestrator(config)

