import subprocess


class Command:
    def __init__(self, command):
        self.command = command
        self.output = ""
        self.error = ""

    def __str__(self):
        return self.command

    def hasProcessed(self):
        return self.output != "" and self.error != ""

    def doProcess(self):
        process = subprocess.Popen([self.command], stdout=subprocess.PIPE)
        self.output, self.error = process.communicate()

    def getOutput(self):
        if not self.hasProcessed():
            self.doProcess()
        return self.output

    def getError(self):
        if not self.hasProcessed():
            self.doProcess()
        return self.error