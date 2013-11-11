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
from linspector.tasks.task import TaskExecutor

logger = getLogger(__name__)


class Job:
    def __init__(self, service, host, members, core, hostgroup):
        self.service = service
        self.host = host
        self.members = members
        self.core = core
        self.hostgroup = hostgroup
        self.job_threshold = 0
        self.job_overall_fails = 0
        self.job_overall_wins = 0
        self.enabled = True
        self.scheduler_job = None
        self.job_id = self.hex_string()
        """
        NONE     job was not executed
        OK       when everything is fine
        WARNING  when a job has errors but not the threshold overridden
        RECOVER  when a job recovers e.g. the threshold decrements (not implemented)
        ERROR    when a jobs threshold is overridden
        UNKNOWN  when a job throws an exception which is not handled by the job itself (not implemented)
        """
        self.status = "NONE"
        self.last_execution = None

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

    def handle_threshold(self, service_threshold, execution_successful):
        if execution_successful:
            if self.job_threshold > 0:
                if "threshold_reset" in self.core and self.core["threshold_reset"]:
                    logger.info("Job " + self.job_id + ", Threshold Reset")
                    self.job_threshold = 0
                else:
                    logger.info("Job " + self.job_id + ", Threshold Decrement")
                    self.job_threshold -= 1

            self.status = "OK"
            self.job_overall_wins += 1
        else:
            self.status = "WARNING"
            self.job_overall_fails += 1
            self.job_threshold += 1

        if self.job_threshold >= service_threshold:
            logger.info("Job " + self.job_id + ", Threshold reached!")
            self.status = "ERROR"

    def handle_tasks(self, msg):
        for member in self.members:
            for task in member.get_tasks():
                if self.status.lower() == task.get_task_type().lower():
                    logger.debug("Executing Task of type: " + self.status)
                    TaskExecutor.Instance().schedule_task(msg, task)

    def handle_call(self):
        logger.debug("handle call")
        logger.debug(self.service)
        if self.enabled:
            self.last_execution = None
            try:
                self.last_execution = JobExecution(self.get_host())
                self.service.execute(self.last_execution)
            except Exception, e:
                logger.debug(e)

            self.last_execution.set_execution_end()
            self.handle_threshold(self.service.get_threshold(), self.last_execution.was_successful())
            logger.info("Job " + self.job_id +
                ", Code: " + str(self.last_execution.get_error_code()) +
                ", Message: " + str(self.last_execution.get_message()))
            self.handle_tasks(self.last_execution.get_response_message(self))
        else:
            logger.info("Job " + self.job_id + " disabled")

    def get_host(self):
        return self.host

    def get_hostgroup(self):
        return self.hostgroup


class JobExecution(object):
    def __init__(self, host):
        self.execution_start = datetime.now()
        self.execution_end = -1
        self.host = host
        self.error_code = -1
        self.message = None
        self.kwargs = None

    def get_host_name(self):
        return self.host

    def get_message(self):
        return self.message

    def get_kwargs(self):
        return self.kwargs

    def set_execution_end(self):
        self.execution_end = datetime.now()

    def get_error_code(self):
        return self.error_code

    def was_successful(self):
        return self.get_error_code() == 0

    def set_result(self, error_code=0, message="", kwargs=None):
        self.error_code = error_code
        self.message = message
        self.kwargs = kwargs

    def get_response_message(self, job):
        msg = str(job.status) + " [" + job.service.get_config_name() + ": " + str(job.job_id) + "] " + \
            str(job.get_hostgroup()) + " " + str(job.get_host())
        if self.get_message() is not None:
            msg += " " + str(self.get_message())
        if self.get_kwargs() is not None:
            msg += " " + str(self.get_kwargs())
        return msg