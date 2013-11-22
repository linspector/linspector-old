"""
The MariaDB task

Uses: http://sourceforge.net/projects/mysql-python

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

import MySQLdb

from logging import getLogger

from linspector.tasks.task import Task

logger = getLogger(__name__)


class MariadbTask(Task):
    def __init__(self, **kwargs):
        super(MariadbTask, self).__init__(**kwargs)

        args = self.get_arguments()

        if "database" in args:
            self.database = args["database"]
        else:
            raise Exception("There is no database set")

        self.table = "default"
        if "table" in args:
            self.table = args["table"]

        self.host = "localhost"
        if "host" in args:
            self.host = args["host"]

        self.port = 3600
        if "port" in args:
            self.port = args["port"]

        self.username = None
        if "username" in args:
            self.username = args["username"]

        self.password = None
        if "password" in args:
            self.password = args["password"]

        self.db = MySQLdb.connect(host=self.host,
                                  port=self.port,
                                  user=self.username,
                                  passwd=self.password,
                                  db=self.database)
        self.cur = self.db.cursor()

    def needs_arguments(self):
        return True

    def execute(self, job_information):
        data = str(job_information.get_job_id()) + "," + \
               str(job_information.get_response_message()) + "," + \
               str(job_information.get_status())

        self.cur.execute("INSERT INTO " + self.table + " (job_id,msg,status) VALUES (" + data + ")")


def create(kwargs):
    return MariadbTask(**kwargs)