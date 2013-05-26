"""
This is what job_function needs as parameter for each job to succesfully 
execute.
"""


class JobInfo:
    def __init__(self, hostgroupname, members, hosts, service, threshold, parent=None):
        self.members = members
        self.hosts = hosts
        self.service = service
        self.threshold = threshold
        self.parent = parent
        self.name = hostgroupname + service.name
        
    def __str__(self):
        return self.name
        
        
    
        
