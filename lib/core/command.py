import subprocess as sp
from subprocess import CalledProcessError
from datetime import datetime as dt

class Command:
    def __init__(self, command):
        self.command = command
        self.output = ""
        self.error = ""
        self.retcode = 0
        self.commandStart=0

    def __str__(self):
        return self.command

    def call(self):
        '''
        self.commandStart = dt.now()
        "called at: "
        process = sp.Popen(stdout=PIPE, *popenargs, **kwargs)
        self.output, self.error = process.communicate()
        self.retcode = process.poll()
        '''
        try:
            print self.command
            self.output=sp.check_output(self.command.split(),stderr=sp.STDOUT)
            
        except CalledProcessError:
            self.error=CalledProcessError.output
            self.retcode = CalledProcessError.returncode
        
    def getOutput(self):
        return self.output

    def getError(self):
        return self.error
        
    def getReturnCode(self):
        return self.retcode
        
