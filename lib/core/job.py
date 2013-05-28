"""
This is what job_function needs as parameter for each job to successfully
execute.
"""

from command import Command


class JobInfo:
    def __init__(self, hostgroupname, members, hosts, service, threshold, parent=None):
        self.members = members
        self.hosts = hosts
        self.service = service
        self.threshold = threshold
        self.parent = parent
        self.name = hostgroupname + "_" + service.name
        self.jobs = []
        
    def __str__(self):
        return self.name
        
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
        print "calling command " + str(service.command) 
        cmd = Command(service.command)
        self.log.d("executing command: " + str(command))
        cmd.call()
        return cmd
        
