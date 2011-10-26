
from yaybu.boiler.type import Instanceable


class ServiceType(Instanceable):
    pass


class BaseService(object):
    __metaclass__ = ServiceType


