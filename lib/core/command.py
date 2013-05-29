import subprocess as sp
from subprocess import Popen
from subprocess import CalledProcessError
from datetime import datetime as dt

class Command:
    def __init__(self, command, log):
        self.command = command
        self.log = log
        self.output = None
        self.error = None
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
            self.commandStart = dt.now()
            self.log.d("calling command " + str(self.command) + " at " + str(self.commandStart)) 
            #self.output=sp.check_output(self.command.split())
            process = Popen(self.command, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
            self.output, self.error = process.communicate()
            self.log.d(str(self.output))
            self.log.d(str(self.error))
            self.retcode = process.poll()
        except CalledProcessError:
            self.error=CalledProcessError.output
            self.retcode = CalledProcessError.returncode
        
        
    def getOutput(self):
        return self.output

    def getError(self):
        return self.error
    
    def getAllOutput(self):
        return str(self.output) + str(self.error) + str(self.retcode)
        
    def getReturnCode(self):
        return self.retcode
        
