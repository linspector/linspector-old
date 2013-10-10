"""
The tcpconnect service. This is to check if a service on a specific port is reachable.

This should just return 0 on success and NOT 0 on error. Just to make internals generic to just report this code and
not use a parser.

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
from linspector.services.service import Service


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

    def execute(self, jobInfo):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            jobInfo.set_errorcode(2)
            jobInfo.set_message("[tcpconnect: " + jobInfo.jobHex + "] Could not create socket to host: " +
                                jobInfo.get_host() + " on port: " + str(self.port) + " (" + str(msg) + ")")

        try:
            sock.connect((jobInfo.get_host(), self.port))
        except socket.error, msg:
            jobInfo.set_errorcode(1)
            jobInfo.set_message("[tcpconnect: " + jobInfo.jobHex + "] Could not establish connection to host: " +
                                jobInfo.get_host() + " on port: " + str(self.port) + " (" + str(msg) + ")")

        if jobInfo.get_errorcode() == -1:
            jobInfo.set_execution_successful(True)
            jobInfo.set_errorcode(0)
            jobInfo.set_message("[tcpconnect: " + jobInfo.jobHex + "] Connection successful established to host: " +
                                jobInfo.get_host() + " on port: " + str(self.port))

        sock.close()


def create(kwargs):
    return TcpconnectService(**kwargs)