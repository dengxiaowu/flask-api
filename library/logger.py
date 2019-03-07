import datetime
import logging  # 引入logging模块
from logging.handlers import RotatingFileHandler
import os


class _Logger:

    def __init__(self, logname=None, homepath=None, logger=False):
        # log的输出格式
        self.fmt = logging.Formatter('%(asctime)s %(levelname)s : %(message)s ')
        self.homepath = homepath if homepath != None else '.'
        self.logname = logname if logname != None else 'mylog'
        self.logger = self.init_logger() if logger else None
        self.sh = self.create_streamhandler()
        self.fh = self.create_filehandler()

    def init_logger(self):
        # 创建一个全局logger
        logger = logging.getLogger(self.logname)
        logger.setLevel(logging.DEBUG)  # Log等级总开关
        return logger

    # 创建一个在终端显示的log处理器
    def create_streamhandler(self):
        if self.logger != None:
            sh = logging.StreamHandler()
            sh.setLevel(logging.DEBUG)
            sh.setFormatter(self.fmt)
            self.logger.addHandler(sh)
            return sh
        else:
            return None

    # 创建一个文件输出处理器
    def create_filehandler(self):
        if self.logger != None:
            # 创建一个handler，用于写入日志文件
            if not os.path.exists(self.homepath + '/logs'):
                os.mkdir(self.homepath + '/logs')
            fh = RotatingFileHandler(self.homepath + '/logs/{}.log'.format(self.logname), maxBytes=100000,
                                     backupCount=10)
            fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
            fh.setFormatter(self.fmt)
            # 第四步，将logger添加到handler里面
            self.logger.addHandler(fh)
            return fh
        else:
            return None

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)

    def rm_streamhandler(self):
        if self.logger != None and self.sh != None:
            self.logger.removeHandler(self.sh)

    def rm_filehandler(self):
        if self.logger != None and self.fh != None:
            self.logger.removeHandler(self.fh)


class LoggerExtend:
    _logger = None
    _name = 'mylog'
    _path = '.'

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, switch):
        if switch:
            self._logger = _Logger(logname=self.name, homepath=self.path, logger=True)


class Logger(LoggerExtend):

    def __init__(self, name=None, path=None, logger=False):
        self.path = path if path != None else '.'
        self.name = name if name != None else 'mylog'
        self.logger = logger

    # 日志输出
    def output_log(self, log_content, level="info"):
        if self.logger != None:
            if level == 'info':
                self.logger.info('{0}'.format(log_content))
            if level == 'error':
                self.logger.error('{0}'.format(log_content))
            if level == 'warn':
                self.logger.warn('{0}'.format(log_content))
            if level == 'debug':
                self.logger.debug('{0}'.format(log_content))
        else:
            print('{0} PRINT {1} : {2}'.format(str(datetime.datetime.today()).replace('.', ',')[:-3], level.upper(),
                                               log_content))

    def removestreamhandler(self):
        if self.logger != None and self.logger.sh != None:
            self.logger.rm_streamhandler()

    def removefilehandler(self):
        if self.logger != None and self.logger.fh != None:
            self.logger.rm_filehandler()
