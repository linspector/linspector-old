"""
The ssh service This is for executing remote shell commands and retrieve the output.

This service is using paramiko (http://www.lag.net/paramiko/).

Copyright (c) 2011-2013 by Johannes Findeisen and Rafael Timmerberg

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

import pprint
import os
from logging import getLogger

import paramiko

from linspector.services.service import Service


logger = getLogger(__name__)


class SshService(Service):
    def __init__(self, **kwargs):
        super(SshService, self).__init__(**kwargs)
        
        args = self.get_arguments()
        if "command" in args:
            self.command = args["command"]
        else:
            raise Exception("There is no command argument")
    
    def needs_arguments(self):
        return True
    
    def execute(self):
        path = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
        key = paramiko.RSAKey.from_private_key_file(path)

        client = paramiko.SSHClient()
        client.get_host_keys().add('hanez.org', 'ssh-rsa', key)
        pprint.pprint(client._host_keys)

        client.connect('hanez.org', username='hanez')

        #self.command.call() ist dann das:
        stdin, stdout, stderr = client.exec_command('ls')
        for line in stdout:
            print '... ' + line.strip('\n')
        client.close()


def create(kwargs):
    return SshService(**kwargs)
