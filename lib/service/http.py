"""
The http service.

This is for checking the availability and output of HTTP services. Basic HTTP
content could be fetched and compared.HTTPS is not validating the server certificate!

This should just return 0 on success and NOT 0 on error. Just to make internals generic
to just report this code and not use a parser.
"""

import urllib
from service import Service


class HttpService(Service):
    def __init__(self, parser, log, **kwargs):
        super(Service, self).__init__(parser)

        if "string" in kwargs:
            self.string = kwargs["string"]
        else:
            log.w("There is no string set to match")

        if "method" in kwargs:
            self.method = kwargs["method"]
        else:
            self.method = "get"

        if "params" in kwargs:
            self.params = kwargs["params"]

        if "path" in kwargs:
            self.path = kwargs["path"]
        elif:
            self.path = "/"

        if "port" in kwargs:
            self.port = kwargs["port"]
        else:
            self.port = "80"

        if "protocol" in kwargs:
            self.protocol = kwargs["protocol"]
        else:
            self.protocol = "http"

    def execute(self):
        params = urllib.urlencode(self.params)
        if self.method is "get":
            f = urllib.urlopen(self.protocol + "://" + self.host + ":" + self.port + self.path + "?%s" % params)
        elif self.method is "post":
            f = urllib.urlopen(self.protocol + "://" + self.host + ":" + self.port + self.path, params)

        #print f.read()