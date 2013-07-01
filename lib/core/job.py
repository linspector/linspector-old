"""
This is what job_function needs as parameter for each job to successfully
execute.
"""

from lib.core.command import Command


def generateId():
    i = 0
    while True:
        yield i
        i += 1


class JobInfo:
    def __init__(self, service):
        self.service = service
        self.name = generateId()
        self.job = None
        
    def __str__(self):
        return "JobInfo " + str(self.name)
        
    def set_logger(self, log):
        self.log = log

    def set_job(self, job):
        self.job = job

    def handle_call(self):
        self.log.d("handle call")
        self.log.d(self.service)
        try:

            self.service._execute()
        except Exception, e:
                self.log.d(e)