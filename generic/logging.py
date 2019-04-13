from logging import handlers
import os


class TimedRotatingFileHandler(handlers.TimedRotatingFileHandler):

    def doRollover(self):

        super().doRollover()
        os.chmod(self.baseFilename, 0o666)
