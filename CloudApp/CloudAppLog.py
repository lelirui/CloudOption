
import logging.handlers
import logging

class CloudAppLog:
    def __init__(self):
        self.logpath='/var/log/CloudApp.log'
        self.logsize=1024*1024*8
        self.logname='CloudApp.log'
    def InitLog(self):
        self.log= logging.getLogger()
        fmt=logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        handle=logging.handlers.RotatingFileHandler(self.logpath,maxBytes=self.logsize,backupCount=1)
        handle.setFormatter(fmt)
        self.log.addHandler(handle)
        self.log.setLevel(logging.INFO)

    def info(cls, msg):
        cls.log.info(msg)
        return


    def warning(cls, msg):
        cls.log.warning(msg)
        return

    def error(cls, msg):
        cls.log.error(msg)
        return