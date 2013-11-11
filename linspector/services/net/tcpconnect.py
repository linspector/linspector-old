"""
The tcpconnect service. This is to check if a TCP service on a specific
port is reachable.

This should just return 0 on success and NOT 0 on error.

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

import socket

from logging import getLogger

from linspector.services.service import Service

logger = getLogger(__name__)


class TcpconnectService(Service):
    def __init__(self, **kwargs):
        super(TcpconnectService, self).__init__(**kwargs)
        
        args = self.get_arguments()
        if "port" in args:
            self.port = args["port"]
        else:
            raise Exception("There is no port set")

    def needs_arguments(self):
        return True

    def execute(self, execution):

        error_code = 0
        msg = "Connection successful established"
        e = "None"

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, e:
            error_code = 2
            msg = "Could not create socket"

        try:
            sock.connect((execution.get_host_name(), self.port))
        except socket.error, e:
            error_code = 1
            msg = "Could not establish connection"

        sock.close()

        d = {"Port": self.port, "Exception": e}
        execution.set_result(error_code, msg, d)


def create(kwargs):
    return TcpconnectService(**kwargs)