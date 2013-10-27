"""
Copyright (c) 2011-2013 "Johannes Findeisen and Rafael Timmerberg"

This file is part of Linspector (http://linspector.org).

Linspector is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from logging import getLogger

from ..core.daemon import Daemon

logger = getLogger(__name__)


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