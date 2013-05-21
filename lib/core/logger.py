import logging
import logging.handlers
import os
import os.path as path


class Logger():
    """Logger class that prints its messages and keeps them also inside a logfile"""

    def __init__(self, logLevel=logging.DEBUG, logfile="/var/log/linspector.log", logfileLevel=logging.DEBUG):
        """
        initializes a new Logger object.

        :param logLevel: the LoggingLevel from the console output (DEBUG default)
        :param logfile:  the file where to log. Logs are rotated by default.
        :param logfileLevel:the LoggingLevel for the file Logger. (DEBUG default)
        """

        logfile = path.expanduser(logfile)
        if not path.exists(path.dirname(logfile)):
            os.makedirs(path.dirname(logfile))

        self.log = logging.getLogger("LinspectorLogger")
        self.log.setLevel(logging.DEBUG)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logLevel)

        fileHandler = logging.handlers.RotatingFileHandler(logfile, maxBytes=2048, backupCount=4)
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

    def w(self, message, category=None):
        self.log.warn(message, category)

    def e(self, message):
        self.log.error(message)

    def c(self, message):
        self.log.critical(message)
        self.log.critical(message)


LOGGER = Logger()


def logVerbose(message, verbose=True):
    LOGGER.d(message)


def logNotice(message, verbose=True):
    LOGGER.i(message)


def logWarning(message):
    LOGGER.w(message)


def logWarningConfig(file="file", missing="missing"):
    logWarning("in " + file + ": The " + missing + " is not defined")


def writeLogToFile(logfile, message):
    pass #always written to file...
