"""
A JSON-RPC backend using HTTP.

Uses: http://deavid.github.io/bjsonrpc/

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

import time

from bjsonrpc.handlers import BaseHandler
from bjsonrpc import createserver

from linspector.backends.backend import Backend


class JsonrpcBackend(Backend):
    def __init__(self, interface, config, **kwargs):
        super(Backend, self).__init__(**kwargs)
        self.interface = interface
        self.config = config

        self.host = "127.0.0.1"
        if config["backends"]["jsonrpc"]["host"]:
            self.host = config["backends"]["jsonrpc"]["host"]
        self.port = 10123
        if config["backends"]["jsonrpc"]["port"]:
            self.port = config["backends"]["jsonrpc"]["port"]

    def run(self):
        while True:
            s = createserver(host=self.host, port=self.port, handler_factory=ServerHandler)
            s.serve()


class ServerHandler(BaseHandler):
    def time(self):
        return time.time()

    def delta(self, start):
        return time.time() - start

    def test(self):
        return "test"