"""
The tcpconnect service. This is to check if a service on a specific port is reachable.

This should just return 0 on success and NOT 0 on error. Just to make internals generic to just report this code and
not use a parser.
"""

import socket
from lib.services.service import Service


class TcpconnectService(Service):
    def __init__(self, **kwargs):
        #Service.__init__(self, **kwargs)
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
            jobInfo.set_errorcode(1)
            jobInfo.set_message("Could not create socket to host: " + jobInfo.get_host() + " to port: " + str(self.port) + " (" + str(msg) + ")")

        try:
            sock.connect((jobInfo.get_host(), self.port))
        except socket.error, msg:
            jobInfo.set_errorcode(2)
            jobInfo.set_message("Could not establish connection to host: " + jobInfo.get_host() + " to port: " + str(self.port) + " (" + str(msg) + ")")

        if jobInfo.get_errorcode() == -1:
            jobInfo.set_execution_successful(True)
            jobInfo.set_errorcode(0)
            jobInfo.set_message("Connection successful established to host: " + jobInfo.get_host() + " to port: " + str(self.port))
        sock.close()


def create(kwargs):
    return TcpconnectService(**kwargs)