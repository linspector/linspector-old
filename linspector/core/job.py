"""
This is what job_function needs as parameter for each job to successfully
execute.

Copyright (c) 2011-2013 "Johannes Findeisen and Rafael Timmerberg"

This file is part of Linspector (http://linspector.org).

Linspector is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from datetime import datetime
from binascii import crc32


def generateId():
    i = 0
    while True:
        yield i
        i += 1


class Job:
    def __init__(self, service, host, members, processors, core):
        self.service = service
        self.host = host
        self.members = members
        self.processors = processors
        self.core = core
        self.jobInfos = []
        self.jobThreshold = 0

    def __str__(self):
        return str(self.__dict__)


    def __hex__(self):
        return hex(crc32(str(self.service) + str(self.host) + str(self.members)))

    def set_logger(self, log):
        self.log = log

    def pretty_string(self):
        ret = self.__hex__()
        if ret[0] == "-":
            ret = ret[3:]
        else:
            ret = ret[2:]
        ret += ": (" + str(self.host) + str(self.service) + str(self.job) + ")"
        return ret

    def set_job(self, job):
        self.job = job

    def handle_threshold(self, jobInfo, serviceThreshold, executionSucessful):
        if executionSucessful:
            if self.jobThreshold > 0:
                self.jobThreshold -= 1
        else:
            self.jobThreshold += 1

        if self.jobThreshold >= serviceThreshold:
            self.log.debug("Threshold reached!")
            self.handle_alarm(jobInfo, self.jobThreshold - serviceThreshold)

    def handle_alarm(self, jobInfo, thresholdOffset):
        for member in self.service.get_hostgroup().get_members():
            #TODO: Put Tasks in a run queue and execute them in a background thread. FIFO! Reduces delay in core.
            for task in member.get_tasks():
                task.execute(jobInfo.get_message(), self.core)

    def handle_call(self):
        self.log.debug("handle call")
        self.log.debug(self.service)
        try:
            jobInfo = JobInfo(self.__hex__(), self.host, self.service)
            self.service._execute(jobInfo)
            jobInfo.set_execution_end()

            self.handle_threshold(jobInfo, self.service.get_threshold(), jobInfo.was_execution_successful())

            self.log.debug("Code: " + str(jobInfo.get_errorcode()) + ", Message: " + str(jobInfo.get_message()))

            self.jobInfos.append(jobInfo)

        except Exception, e:
            self.log.debug(e)


class JobInfo(object):
    def __init__(self,jobHex, host, service):
        self.id = generateId()
        self.jobHex = jobHex
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