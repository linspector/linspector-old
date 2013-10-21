"""
The Linspector JSON-RPC backend.

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

import json
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

        ServerHandler.interface = interface
        ServerHandler.config = config

    def run(self):
        while True:
            server = createserver(host=self.host, port=self.port, handler_factory=ServerHandler)
            server.serve()


class ServerHandler(BaseHandler):
    interface = None
    config = None

    def get_job_list(self):
        job_list = ServerHandler.interface.get_job_list()
        return json.dumps(job_list, ensure_ascii=False)

    def get_job_list_by_hostgroup(self, hostgroup):
        job_list = ServerHandler.interface.get_job_list_by_hostgroup(hostgroup)
        return json.dumps(job_list, ensure_ascii=False)

    def get_job_list_by_host(self, host):
        job_list = ServerHandler.interface.get_job_list_by_host(host)
        return json.dumps(job_list, ensure_ascii=False)

    def get_job_count(self):
        job_count = ServerHandler.interface.get_job_count()
        return json.dumps(job_count, ensure_ascii=False)

    def get_job_count_by_hostgroup(self, hostgroup):
        job_count = ServerHandler.interface.get_job_count_by_hostgroup(hostgroup)
        return json.dumps(job_count, ensure_ascii=False)

    def get_job_count_by_host(self, host):
        job_count = ServerHandler.interface.get_job_count_by_host(host)
        return json.dumps(job_count, ensure_ascii=False)

    def get_job_info_by_id(self, job_hex):
        job = ServerHandler.interface.find_job_by_hex_string(job_hex)
        job_dict = ServerHandler.interface.get_job_info_dict(job)
        return json.dumps(job_dict, ensure_ascii=False)

    def set_job_enabled(self, job_hex, enabled=True):
        job = ServerHandler.interface.find_job_by_hex_string(job_hex)
        job.set_enabled(enabled)
        return True

    def get_hostgroup_list(self):
        pass

    def get_hostgroup_count(self):
        pass

    def get_host_list(self):
        pass

    def get_host_list_by_hostgroup(self, hostgroup):
        pass

    def get_host_count(self):
        pass

    def get_host_count_by_hostgroup(self, hostgroup):
        pass

    def get_services_by_hostgroup(self, hostgroup):
        pass

    def get_services_by_host(self, host):
        pass

    def get_service_count_by_hostgroup(self, hostgroup):
        pass

    def get_service_count_by_host(self, host):
        pass