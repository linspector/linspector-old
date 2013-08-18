from ..core import logger
from ..core.daemon import Daemon

"""
TODO: Think about, that daemonizing this software is not our goal but when we want to that, this needs a rewrite and
should maybe move over to the daemon frontend. daemon.py will remain the the base for this and should stay in lib/core .
Since a daemon it normally not a frontend we should think about how to handle this. When daemonizing a real frontend
like "Lish" will make no sense but a frontend like "https" or "xmpp" could be useful anyway...
"""


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