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

import subprocess as sp

from subprocess import Popen
from subprocess import CalledProcessError
from datetime import datetime as dt
from logging import getLogger

logger = getLogger(__name__)

#TODO: Move this to shell.py service file. this definitely is shell execution. (hanez)


class Command:
    def __init__(self, command):
        self.command = command
        self.output = None
        self.error = None
        self.retcode = 0
        self.commandStart = 0

    def __str__(self):
        return self.command

    def call(self):

        # self.commandStart = dt.now()
        # "called at: "
        # process = sp.Popen(stdout=PIPE, *popenargs, **kwargs)
        # self.output, self.error = process.communicate()
        # self.retcode = process.poll()

        try:
            self.commandStart = dt.now()
            logger.info("calling command " + str(self.command) + " at " + str(self.commandStart))
            #self.output=sp.check_output(self.command.split())
            process = Popen(self.command, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
            self.output, self.error = process.communicate()
            logger.debug(str(self.output))
            logger.debug(str(self.error))
            self.retcode = process.poll()
        except CalledProcessError:
            self.error = CalledProcessError.output
            self.retcode = CalledProcessError.returncode

    def getOutput(self):
        return self.output

    def getError(self):
        return self.error
    
    def getAllOutput(self):
        return str(self.output) + str(self.error) + str(self.retcode)
        
    def getReturnCode(self):
        return self.retcode