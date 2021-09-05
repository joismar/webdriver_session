import logging
import sys


class LoggerMeta(type):

    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            instance = super().__call__(*args, **kwargs)
            self._instances[self] = instance
        return self._instances[self]


class Logger(metaclass=LoggerMeta):

    def __init__(self, name):
        self.__handler = None
        self.__log = None
        self.name = name
        self.__setup()

    def __setup(self):
        self.__log = logging.getLogger(self.name)
        self.__log.level = logging.DEBUG
        self.__handler = logging.StreamHandler(sys.stdout)
        self.__log.addHandler(self.__handler)

    @property
    def log(self):
        return self.__log

    @classmethod
    def destroy(self):
        self.__handler.removeHandler(self.__handler)
