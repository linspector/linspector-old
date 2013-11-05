"""
Get content via http and check for a string in the content.

Uses: https://github.com/kennethreitz/requests

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

import requests

from logging import getLogger

from linspector.services.service import Service

logger = getLogger(__name__)


class HttpCodeService(Service):
    def __init__(self, **kwargs):
        super(HttpCodeService, self).__init__(**kwargs)

        args = self.get_arguments()
        if "code" in args:
            self.code = args["code"]
        else:
            raise Exception("There is no code set")

        self.method = "get"
        if "method" in args:
            self.method = args["method"]

        self.params = None
        if "params" in args:
            self.params = kwargs["params"]

        self.path = "/"
        if "path" in args:
            self.path = kwargs["path"]

        self.port = "80"
        if "port" in args:
            self.port = kwargs["port"]

        self.protocol = "http"
        if "protocol" in args:
            self.protocol = kwargs["protocol"]

    def needs_arguments(self):
        return True

    def execute(self, job):
        r = requests.get(self.protocol + "://" + job.get_host() + ":" + self.port + self.path)

        if self.code != r.status_code:
            job.set_errorcode(1)
            job.set_message("[http/code: " + job.jobHex + "] Failed on host: " + job.get_host() +
                            " Expected Code: " + str(self.code) + ", Code was: " + str(r.status_code))

        if job.get_errorcode() == -1:
            job.set_execution_successful(True)
            job.set_errorcode(0)
            job.set_message("[http/code: " + job.jobHex + "] Success on host: " + job.get_host() +
                            " Expected Code: " + str(self.code) + ", Code was: " + str(r.status_code))


def create(kwargs):
    return HttpCodeService(**kwargs)