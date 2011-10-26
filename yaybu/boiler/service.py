from twisted.application import service

from yaybu.boiler.type import Instanceable


class ServiceType(Instanceable):
    pass


class BaseService(object, service.MultiService):
    __metaclass__ = ServiceType

    def __init__(self):
        service.MultiService.__init__(self)

