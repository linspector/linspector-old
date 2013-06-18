"""
The shell service. This is for executing local shell commands and retrieve the output.
"""

from service import Service


class ShellService(Service):
    def __init__(self, **kwargs):
        super(ShellService, self).__init__(**kwargs)
        
        args = self.get_arguments()
        if "command" in args:
            self.command = args["command"] 
        else:
            raise Exception("There is no command argument")
        
    def needs_arguments(self):
        return True 

    def execute(self):
        self.command.call()


def create(kwargs):
    return ShellService(**kwargs)