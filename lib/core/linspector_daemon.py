from ..core import logger
from ..core.daemon import Daemon


class LinspectorDaemon(Daemon):
    def run(self):
        while True:
            try:
                a = 2
                logger.writeLogToFile(_logfile, "Running!")
                print "running!"
            except Exception as err:
                #logger.writeLogToFile(_logfile, str(err))
                print "failed"
                sys.exit(1)
            time.sleep(1)