"""
A JSON-RPC backend using HTTP.

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

from linspector.backends.backend import Backend


class JsonrpcBackend(Backend):
    def __init__(self, interface, **kwargs):
        super(Backend, self).__init__(**kwargs)
        self.interface = interface

    def run(self):
        while True:
            print "hello from JsonrpcBackend thread..."
            time.sleep(5)
