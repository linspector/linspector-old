"""
The shell service. This is for executing services as shell commands
and don't use a builtin function. This is useful to be free to do what you want.
"""

from service import Service


class ShellService(Service):
    def __init__(self, parser, log, **kwargs):
        super(Service, self).__init__(parser)
        if "command" in kwargs:
            self.command = kwargs["command"]
        else:
            log.w("There is no command")

    def execute(self):
        self.command.call()