from datetime import datetime

DEBUG = "[debug]"
NOTICE = "[notice]"
WARNING = "[warning]"


def logVerbose(message, verbose=True):
    if verbose:
        print DEBUG + " " + str(message)


def logNotice(message, verbose=True):
    if verbose:
        print NOTICE + " " + str(message)


def logWarning(message):
    print WARNING + " " + message


def logWarningConfig(thefile="file", missing="missing"):
    logWarning("in " + thefile + ": The " + missing + " is not defined")


def writeLogToFile(logfile, message):
    f = open(logfile, 'a')
    f.write("[" + str(datetime.now()) + "] " + message + '\n')
    f.close()


class Logger:
    def __init__(self, logfile="/dev/null"):
        self.logfile = logfile

    def logSomething(self, message, verbose=False):
        f = open(self.logfile, 'a')
        f.write("[" + str(datetime.now()) + "] " + message + '\n')
        f.close()

