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
    def __init__(self, **kwargs):
        super(HttpService, self).__init__(**kwargs)
        
        args = self.get_arguments()
        
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
            

    def execute(self):
        params = urllib.urlencode(self.params)
        if self.method is "get":
            f = urllib.urlopen(self.protocol + "://" + self._host + ":" + self.port + self.path + "?%s" % params)
        elif self.method is "post":
            f = urllib.urlopen(self.protocol + "://" + self._host + ":" + self.port + self.path, params)

        #print f.read()
        
def create(**kwargs):
    return HttpService(**kwargs)