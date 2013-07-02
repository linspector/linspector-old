"""
This is what job_function needs as parameter for each job to successfully
execute.
"""
from datetime import datetime

def generateId():
    i = 0
    while True:
        yield i
        i += 1

class Job:
    def __init__(self, service):
        self.service = service
        self.jobInfos = []
        self.hostThreshold = {}
        for host in service.get_hostgroup().get_hosts():
            self.hostThreshold[host] = service.get_threshold()
        

    def __str__(self):
        return str(self.__dict__)

    def set_logger(self, log):
        self.log = log

    def set_job(self, job):
        self.job = job

    def handle_call(self):
        self.log.d("handle call")
        self.log.d(self.service)

        for host in self.service.get_hostgroup().get_hosts():
            try:
                jobInfo = JobInfo(host, self.service)
                result = self.service._execute(host)
                jobInfo.set_result(result)
                jobInfo.set_successfull(self.service.was_execution_successful())
                jobInfo.set_execution_end()

            except Exception, e:
                self.log.d(e)


class JobInfo:
    def __init__(self, host, service):
        self.id = generateId()
        self.host = host
        self.service = service
        self.executionBegin = datetime.now()

    def set_result(self, result):
        self.result = result

    def set_execution_end(self):
        self.executionEnd = datetime.now()

    def set_execution_successful(self, successful):
        self.executionSuccess = successful


