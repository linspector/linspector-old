"""
This is what job_function needs as parameter for each job to successfully
execute.

Copyright (c) 2011-2013 by Johannes Findeisen and Rafael Timmerberg

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
from logging import getLogger

logger = getLogger(__name__)


class Job:
    def __init__(self, service, host, members, processors, core, task_list, hostgroup):
        self.service = service
        self.host = host
        self.members = members
        self.processors = processors
        self.core = core
        self.task_list = task_list
        self.hostgroup = hostgroup
        self.job_infos = []
        self.job_index = -1
        self.job_info_size = 10
        self.job_threshold = 0
        self.job_overall_fails = 0
        self.job_overall_wins = 0
        self.enabled = True
        self.result = None
        self.scheduler_job = None
        self.execution_begin = datetime.now()
        self.execution_end = None
        self.errorcode = -1
        self.message = None
        self.execution_success = False
        self.jobHex = self.hex_string()
        """
        NONE     job was not executed
        OK       when everything is fine
        WARNING  when a job has errors but not the threshold overridden
        RECOVER  when a job recovers e.g. the threshold decrements (not implemented)
        ERROR    when a jobs threshold is overridden
        UNKNOWN  when a job throws an exception which is not handled by the job itself (not implemented)
        """
        self.status = "NONE"

    def __str__(self):
        return str(self.__dict__)

    def __hex__(self):
        return hex(crc32(str(self.hostgroup) + str(self.host) + str(self.service)))

    def hex_string(self):
        ret = self.__hex__()
        if ret[0] == "-":
            ret = ret[3:]
        else:
            ret = ret[2:]
        while len(ret) < 8:
            ret = "0" + ret
        return ret

    def set_job(self, scheduler_job):
        self.scheduler_job = scheduler_job

    def set_enabled(self, enabled=True):
        self.enabled = enabled

    def add_job_info(self, job_info):
        self.job_index += 1
        if self.job_index > self.job_info_size:
            self.job_index = 0
        self.job_infos[self.job_index] = job_info

    def handle_threshold(self, service_threshold, execution_sucessful):
        if execution_sucessful:
            if self.job_threshold > 0:
                if "threshold_reset" in self.core and self.core["threshold_reset"]:
                    logger.info("Job " + self.hex_string() + ", Threshold Reset")
                    self.job_threshold = 0
                else:
                    logger.info("Job " + self.hex_string() + ", Threshold Decrement")
                    self.job_threshold -= 1

            self.status = "OK"
            self.job_overall_wins += 1
        else:
            self.status = "WARNING"
            self.job_overall_fails += 1
            self.job_threshold += 1

        if self.job_threshold >= service_threshold:
            logger.info("Job " + self.hex_string() + ", Threshold reached!")
            self.status = "ERROR"
            self.handle_alarm()

    def handle_alarm(self):
        for member in self.members:
            self.task_list.execute_task_infos(self.status + " " + self.get_message(), member.get_tasks())

    def handle_call(self):
        logger.debug("handle call")
        logger.debug(self.service)
        if self.enabled:
            try:
                self.service.execute(self)
                self.set_execution_end()
                self.handle_threshold(self.service.get_threshold(), self.was_execution_successful())
                logger.info("Job " + self.hex_string() +
                            ", Code: " + str(self.get_errorcode()) +
                            ", Message: " + str(self.get_message()))

                self.reset_errorcode(-1)
                self.set_execution_successful(False)
            except Exception, e:
                logger.debug(e)
        else:
            logger.info("Job " + self.hex_string() + " disabled")

    def reset_errorcode(self, errorcode):
        self.errorcode = errorcode

    def get_host(self):
        return self.host

    def set_result(self, result):
        self.result = result

    def set_execution_end(self):
        self.execution_end = datetime.now()

    def set_execution_successful(self, successful):
        self.execution_success = successful

    def was_execution_successful(self):
        return self.execution_success

    def set_message(self, msg):
        self.message = msg

    def get_message(self):
        return self.message

    def set_errorcode(self, errcode):
        self.errorcode = errcode

    def get_errorcode(self):
        return self.errorcode