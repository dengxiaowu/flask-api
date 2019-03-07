import logging
from enum import Enum

from configs.config import configs


class AppLog:
    level = Enum('level',
                 {
                     'debug': logging.DEBUG,
                     'info': logging.INFO,
                     'warning': logging.WARNING,
                     'error': logging.ERROR,
                     'critical': logging.CRITICAL
                 }
                 )

    loggers = None

    lvl = None

    def __init__(self, name):

        self.loggers = logging.getLogger(name)

        self.loggers.setLevel(logging.DEBUG)

        self.setLogHandle()

    def setLogHandle(self):
        log_path = configs['log']['path']
        fhandler = logging.FileHandler(log_path, 'a', 'utf-8')

        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

        fhandler.setFormatter(formatter)

        fhandler.setLevel(logging.DEBUG)

        console = logging.StreamHandler()

        console.setFormatter(formatter)

        console.setLevel(logging.ERROR)

        self.loggers.addHandler(fhandler)

        self.loggers.addHandler(console)

    def __getattr__(self, name):
        if (name in ('debug', 'info', 'warn', 'error', 'critical')):
            self.lvl = self.level[name].value
            return self
        else:
            raise AttributeError('Attr not Correct')

    def __call__(self, msg):

        self.loggers.log(self.lvl, msg)


if __name__ == '__main__':
    AppLog('test').error('test info')
