"""
The ssh service This is for executing remote shell commands and retrieve the output.

This service is using paramiko (http://www.lag.net/paramiko/).
"""

import paramiko
import pprint
import os
from service import Service


class SshService(Service):
    def __init__(self, parser, log, **kwargs):
        super(Service, self).__init__(parser)
        if "command" in kwargs:
            self.command = kwargs["command"]
        else:
            log.w("There is no command")

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


# def main():
#     # service = SshService(parser, log, command='uptime')
#     return
#
# if __name__ == "__main__":
#     main()