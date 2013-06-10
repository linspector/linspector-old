"""
The shell service. This is for executing local shell commands and retrieve the output.
"""

from service import Service


class ShellService(Service):
    def __init__(self, parser, log, **kwargs):
        super(Service, self).__init__(parser)
        if "command" in kwargs:
            self.command = kwargs["command"]
        else:
            log.w("There is no command")
            raise

    def execute(self):
        self.command.call()