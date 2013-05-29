"""
This is what job_function needs as parameter for each job to successfully
execute.
"""

from command import Command

def generateId():
    i=0
    while True:
      yield i
      i+=1

class JobInfo:
    def __init__(self, hostgroupname, members, hosts, hostServices, threshold, parent=None):
        self.members = members
        self.hosts = hosts
        self.hostServices = hostServices
        self.threshold = threshold
        self.parent = parent
        self.name = generateId()
        #self.name = hostgroupname +  str([str("_" + s.service.name ) for s in hostServices])
        self.jobs = []
        
    def __str__(self):
        return "JobInfo " + str(self.name)
        
    def setLogger(self, log):
        self.log = log
        
    def appendJob(self, job):
        self.jobs.append(job)
        
    def getNextExecutionTime(self):
        nextExecution = None
        for job in self.jobs:
            jobExec = job.trigger.get_next_fire_time()
            if nextExecution is None or nextExecution > jobExec:
                nextExecution = jobExec
        return nextExecution
        
    def handleCall(self):
        self.log.d("handle call")
        self.log.d(self.hostServices)
        try:
            
            for hs in self.hostServices:
                self.log.d(str(hs))
                cmd=Command(hs.service.command, self.log)
                cmd.call()
                self.log.d(cmd.getAllOutput())
        except Exception:
                self.log.d(Exception)
        
        
        #must find real service command stored in hosts...
        #but because of error, mentioned in NOTES,ruff, there is no ping i.e.

        #cmd = Command(service.command)
        #self.log.d("executing command: " + str(command))
        #cmd.call()
        #return cmd
        
