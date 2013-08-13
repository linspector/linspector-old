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
    def __init__(self, service, host):
        self.service = service
        self.host = host
        self.jobInfos = []
        self.jobThreshold = 0

    def __str__(self):
        return str(self.__dict__)

    def set_logger(self, log):
        self.log = log

    def set_job(self, job):
        self.job = job

    def handle_threshold(self, serviceThreshold, executionSucessful):
        if executionSucessful:
            pass
        else:
            self.jobThreshold += 1

        if self.jobThreshold >= serviceThreshold:
            self.handle_alarm(self.jobThreshold-serviceThreshold)

    def handle_alarm(self, threholdOffset):
        pass

    def handle_call(self):
        self.log.d("handle call")
        self.log.d(self.service)
        try:
            jobInfo = JobInfo(self.host, self.service)
            result = self.service._execute(self.host)
            jobInfo.set_result(result)
            jobInfo.set_successfull(self.service.was_execution_successful())
            jobInfo.set_execution_end()

            self.handle_threshold(self.service.get_threshold(), self.service.was_execution_successful())


            self.jobInfos.append(jobInfo)


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


