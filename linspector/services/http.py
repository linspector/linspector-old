"""
The http service.

This is for checking the availability and output of HTTP services. Basic HTTP
content could be fetched and compared.HTTPS is not validating the server
certificate!

This should just return 0 on success and NOT 0 on error. Just to make internals
generic to just report this code and not use a parser.

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

import urllib

from logging import getLogger

from linspector.services.service import Service

logger = getLogger(__name__)


class HttpService(Service):
    def __init__(self, **kwargs):
        super(HttpService, self).__init__(**kwargs)

        args = self.get_arguments()
        if "content" in args:
            self.content = args["content"]
        else:
            raise Exception("There is no content set")
        
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

    def execute(self, jobInfo):
        params = urllib.urlencode(self.params)

        if self.method is "get":
            f = urllib.urlopen(self.protocol + "://" + self._host + ":" + self.port + self.path + "?%s" % params)
        elif self.method is "post":
            f = urllib.urlopen(self.protocol + "://" + self._host + ":" + self.port + self.path, params)

        if self.content not in f.read():
            jobInfo.set_errorcode(1)
            jobInfo.set_message("[http: " + jobInfo.jobHex + "] Content not found on host: " +
                                jobInfo.get_host() + " on port: " + str(self.port))
        elif jobInfo.get_errorcode() == -1:
            jobInfo.set_execution_successful(True)
            jobInfo.set_errorcode(0)
            jobInfo.set_message("[http: " + jobInfo.jobHex + "] Content found on host: " +
                                jobInfo.get_host() + " on port: " + str(self.port))


def create(kwargs):
    return HttpService(**kwargs)