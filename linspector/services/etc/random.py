"""
Dummy service creating random data; for debugging and testing

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

import os


from logging import getLogger

from linspector.services.service import Service

logger = getLogger(__name__)


class RandomService(Service):

    def __init__(self, **kwargs):
        super(RandomService, self).__init__(**kwargs)

        args = self.get_arguments()

        self.count = 10
        if "count" in args:
            self.count = args["count"]

        self.length = 1024
        if "length" in args:
            self.length = args["length"]

        self.fail = False
        if "fail" in args:
            self.fail = args["fail"]

    def needs_arguments(self):
        return False

    def execute(self, execution):

        for i in range(self.count):
            os.urandom(self.length)

        d = {"Fail": str(self.fail), "Count": str(self.count), "Length": str(self.length)}
        error_code = 0
        msg = "Success"
        if self.fail:
            error_code = 1
            msg = "Failed"
        execution.set_result(error_code, msg, d)


def create(kwargs):
    return RandomService(**kwargs)