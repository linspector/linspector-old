"""
The tcpconnect service. This is to check if a service on a specific port is reachable.

This should just return 0 on success and NOT 0 on error. Just to make internals generic to just report this code and
not use a parser.
"""

import socket
from service import Service


class TcpconnectService(Service):
    def __init__(self, parser, log, **kwargs):
        super(Service, self).__init__(parser)

        if "port" in kwargs:
            self.port = kwargs["port"]
        else:
            log.w("There is no port set")
            raise

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