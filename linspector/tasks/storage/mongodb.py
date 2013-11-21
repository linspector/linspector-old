"""
The MongoDB task

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
from pymongo import MongoClient

from linspector.tasks.task import Task

logger = getLogger(__name__)


class MongodbTask(Task):
    def __init__(self, **kwargs):
        super(MongodbTask, self).__init__(**kwargs)

        args = self.get_arguments()

        if "database" in args:
            self.database = args["database"]
        else:
            raise Exception("There is no database set")

        if "collection" in args:
            self.collection = args["collection"]
        else:
            raise Exception("There is no collection set")

        self.host = "localhost"
        if "host" in args:
            self.host = args["host"]

        self.port = 27017
        if "port" in args:
            self.port = args["port"]

        self.client = MongoClient(self.host, self.port)

    def execute(self, job_information):
        pass


def create(kwargs):
    return MongodbTask(**kwargs)