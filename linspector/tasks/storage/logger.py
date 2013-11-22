"""
The Logger task - Logs data to a file

Copyright (c) 2011-2013 by Johannes Findeisen and Rafael Timmerberg

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

from linspector.tasks.task import Task

logger = getLogger(__name__)


class LoggerTask(Task):
    def __init__(self, **kwargs):
        super(LoggerTask, self).__init__(**kwargs)

        args = self.get_arguments()

        if "directory" in args:
            self.directory = args["directory"]
        else:
            raise Exception("There is no directory set")

        self.file = "data.log"
        if "file" in args:
            self.file = args["file"]

    def needs_arguments(self):
        return True

    def execute(self, job_information):
        f = open(self.directory + self.file, 'a')
        f.write(job_information.get_response_message() + '\n')
        f.close()


def create(kwargs):
    return LoggerTask(**kwargs)