import logging
import logging.handlers
import os
import os.path as path


class Logger():
    """
    Logger class that prints its messages and keeps them also inside a logfile
    """

    def __init__(self, logfile="./linspector.log", logLevel=logging.DEBUG, logfileLevel=logging.DEBUG):
        """
        initializes a new Logger object.

        :param logLevel: the LoggingLevel from the console output (DEBUG default)
        :param logfile: the file where to log. Logs are rotated by default.
        :param logfileLevel: the LoggingLevel for the file Logger. (DEBUG default)
        """

        logfile = path.expanduser(logfile)
        if not path.exists(path.dirname(logfile)):
            os.makedirs(path.dirname(logfile))

        self.log = logging.getLogger("LinspectorLogger")
        self.log.setLevel(logging.DEBUG)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logLevel)

        fileHandler = logging.handlers.RotatingFileHandler(logfile, maxBytes=1024000, backupCount=4)
        fileHandler.setLevel(logfileLevel)

        consoleFormatter = logging.Formatter('[%(levelname)s]: %(message)s')
        fileFormatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')

        consoleHandler.setFormatter(consoleFormatter)
        fileHandler.setFormatter(fileFormatter)

        self.log.addHandler(consoleHandler)
        self.log.addHandler(fileHandler)

    def d(self, message):
        self.log.debug(message)

    def i(self, message):
        self.log.info(message)

    def w(self, message):
        self.log.warn(message)

    def e(self, message):
        self.log.error(message)

    def c(self, message):
        self.log.critical(message)

    def close(self):
        logging.shutdown()