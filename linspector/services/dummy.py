"""
Dummy service for debugging and testing

This should just return 0 on success and 1 on error.

Example json service config for fail:

{
    "class": "dummy",
    "args": { "sleep": 3, "fail": 1 },
    "periods": ["fast"],
    "threshold": 3
}

For Success:

{
    "class": "dummy",
    "args": { "sleep": 3, "fail": 0 },
    "periods": ["fast"],
    "threshold": 3
}

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

import time

from logging import getLogger

from linspector.services.service import Service

logger = getLogger(__name__)


class DummyService(Service):
    def __init__(self, **kwargs):
        super(DummyService, self).__init__(**kwargs)

        args = self.get_arguments()

        self.sleep = 1
        if "sleep" in args:
            self.port = args["sleep"]

        self.fail = 0
        if "fail" in args:
            self.fail = args["fail"]

    def needs_arguments(self):
        return False

    def execute(self, jobInfo):

        time.sleep(self.sleep)

        if self.fail > 0:
            jobInfo.set_errorcode(1)
            jobInfo.set_message("[dummy: " + jobInfo.jobHex + "] Failed on host: " + jobInfo.get_host() +
                                " Sleep: " + str(self.sleep) + " Fail: " + str(self.fail))

        if jobInfo.get_errorcode() == -1:
            jobInfo.set_execution_successful(True)
            jobInfo.set_errorcode(0)
            jobInfo.set_message("[dummy: " + jobInfo.jobHex + "] Success on host: " + jobInfo.get_host() +
                                " Sleep: " + str(self.sleep) + " Fail: " + str(self.fail))


def create(kwargs):
    return DummyService(**kwargs)