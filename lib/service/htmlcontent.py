"""
The htmlcontent service in pure Python. STUPID NAME!!!

This should just return 0 on success and NOT 0 on error. Just to make internals generic to just report this code and
not use a parser.
"""

# http://pycurl.sourceforge.net/ --- seems old...
# http://www.angryobjects.com/2011/10/15/http-with-python-pycurl-by-example/
#
# maybe better: http://docs.python.org/2/library/urllib.html
#
# or look at tcpconnect.py! could be useful to.

import socket
import sys
from service import Service


class HtmlcontentService(Service):
    def __init__(self, parser, log, **kwargs):
        super(Service, self).__init__(parser)

        if "string" in kwargs:
            self.string = kwargs["string"]
        else:
            log.w("There is no string set to match")

    def execute(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            sys.stderr.write("[ERROR] %s\n" % msg[1])
            sys.exit(1)

        try:
            sock.connect((self.host, self.port))
        except socket.error, msg:
            sys.stderr.write("[ERROR] %s\n" % msg[1])
            sys.exit(2)

        sock.send("GET %s HTTP/1.0\r\nHost: %s\r\n\r\n" % (self.path, self.host))

        data = sock.recv(1024)
        string = ""
        while len(data):
            string = string + data
            data = sock.recv(1024)
        sock.close()
        #print string
        # make substring in string compare here. regex or so...
