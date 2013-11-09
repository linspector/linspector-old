"""
Dummy service for debugging and testing

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
import random

from logging import getLogger

from linspector.services.service import Service

logger = getLogger(__name__)


class DummyService(Service):
    """
    This should just return 0 on success and 1 on error.

    Example json service config for fail:
    {
        "class": "dummy",
        "args": { "sleep": 3, "fail": true },
        "periods": ["fast"],
        "threshold": 3
    }

    For Success:
    {
        "class": "dummy",
        "args": { "sleep": 3, "fail": false },
        "periods": ["fast"],
        "threshold": 3
    }
    """
    def __init__(self, **kwargs):
        super(DummyService, self).__init__(**kwargs)

        args = self.get_arguments()

        self.sleep = random.randint(3, 15)
        if "sleep" in args:
            self.sleep = args["sleep"]

        self.fail = False
        if "fail" in args:
            self.fail = args["fail"]

    def needs_arguments(self):
        return False

    def execute(self, job):

        time.sleep(self.sleep)

        if self.fail:
            job.set_errorcode(1)
            job.set_message("[etc/dummy: " + job.jobHex + "] Failed on host: " + job.get_host() +
                            " Sleep: " + str(self.sleep) + " Fail: " + str(self.fail))

        if job.get_errorcode() == -1:
            job.set_execution_successful(True)
            job.set_errorcode(0)
            job.set_message("[etc/dummy: " + job.jobHex + "] Success on host: " + job.get_host() +
                            " Sleep: " + str(self.sleep) + " Fail: " + str(self.fail))


def create(kwargs):
    return DummyService(**kwargs)