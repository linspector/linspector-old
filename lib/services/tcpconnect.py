"""
The tcpconnect service. This is to check if a service on a specific port is reachable.

This should just return 0 on success and NOT 0 on error. Just to make internals generic to just report this code and
not use a parser.
"""

import socket
from lib.config.services import Service
from service import Service


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

    def execute(self, log):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            log.w("%s\n" % msg[1])
            self.errorcode = 1

        try:
            sock.connect((self.host, self.port))
        except socket.error, msg:
            log.w("%s\n" % msg[1])
            self.errorcode = 2

        sock.close()
        return


def create(kwargs):
    return TcpconnectService(**kwargs)