"""
This is what job_function needs as parameter for each job to successfully
execute.
"""

import subprocess


class JobInfo:
    def __init__(self, hostgroupname, members, hosts, service, threshold, parent=None):
        self.members = members
        self.hosts = hosts
        self.service = service
        self.threshold = threshold
        self.parent = parent
        self.name = hostgroupname + "_" + service.name + " " + service.command
        
    def __str__(self):
        return self.name
        
    def setLogger(self, log):
        self.log = log
        
    def handleCall(self):
        #p = subprocess.Popen("df -h", stdout=subprocess.PIPE, shell=True)
        #(output, err) = p.communicate()
        #print output
        pass