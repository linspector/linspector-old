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
    def __init__(self, service, host, members, processors):
        self.service = service
        self.host = host
        self.members = members
        self.processors = processors
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
            if self.jobThreshold > 0:
                self.jobThreshold -= 1
        else:
            self.jobThreshold += 1

        if self.jobThreshold >= serviceThreshold:
            self.log.d("Threshold reached!")
            self.handle_alarm(self.jobThreshold - serviceThreshold)

    def handle_alarm(self, thresholdOffset):
        pass

    def handle_call(self):
        self.log.d("handle call")
        self.log.d(self.service)
        try:
            jobInfo = JobInfo(self.host, self.service)
            self.service._execute(jobInfo)
            jobInfo.set_execution_end()

            self.handle_threshold(self.service.get_threshold(), jobInfo.was_execution_successful())

            self.log.d("Error Code: " + str(jobInfo.get_errorcode()) + ", Message: " + str(jobInfo.get_message()))

            self.jobInfos.append(jobInfo)

        except Exception, e:
            self.log.d(e)


class JobInfo(object):
    def __init__(self, host, service):
        self.id = generateId()
        self.host = host
        self.service = service
        self.executionBegin = datetime.now()
        self._errorcode = -1
        self._message = None
        self._executionSuccess = False

    def get_host(self):
        return self.host

    def set_result(self, result):
        self.result = result

    def set_execution_end(self):
        self.executionEnd = datetime.now()

    def set_execution_successful(self, successful):
        self._executionSuccess = successful

    def was_execution_successful(self):
        return self._executionSuccess

    def set_message(self, msg):
        self._message = msg

    def get_message(self):
        return self._message

    def set_errorcode(self, errcode):
        self._errorcode = errcode

    def get_errorcode(self):
        return self._errorcode