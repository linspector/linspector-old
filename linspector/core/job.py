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

"""
TODO:

 - tasks should not be normal python threads; they should be created using the
   multiprocessing library to make sure we could use more then one cpu core.
   if we switch to celery for task execution at some time we even could use
   celery for task execution. currently we support only one core when running
   linspector... :(
"""

from datetime import datetime
from binascii import crc32
from logging import getLogger
from linspector.tasks.task import TaskExecutor

logger = getLogger(__name__)


class LinspectorJob:
    def __init__(self, service, host, members, core, hostgroup):
        self.service = service
        self.host = host
        self.members = members
        self.core = core
        self.hostgroup = hostgroup
        self.job_threshold = 0
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
        self.job_information = JobInformation(self.job_id, hostgroup, host, service, members)

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

    def get_job_id(self):
        return self.job_id

    def set_job(self, scheduler_job):
        self.scheduler_job = scheduler_job

    def set_enabled(self, enabled=True):
        self.enabled = enabled

    def handle_threshold(self, service_threshold, execution_successful):
        if execution_successful:
            if self.job_threshold > 0:
                if "threshold_reset" in self.core and self.core["threshold_reset"]:
                    logger.info("Job " + self.get_job_id() + ", Threshold Reset")
                    self.job_threshold = 0
                else:
                    logger.info("Job " + self.get_job_id() + ", Threshold Decrement")
                    self.job_threshold -= 1

            self.status = "OK"
            self.job_information.set_status(self.status)
            self.job_information.inc_job_overall_wins()
        else:
            self.status = "WARNING"
            self.job_information.set_status(self.status)
            self.job_information.inc_job_overall_fails()
            self.job_threshold += 1

        if self.job_threshold >= service_threshold:
            logger.info("Job " + self.get_job_id() + ", Threshold reached!")
            self.status = "ERROR"
            self.job_information.set_status(self.status)

    def handle_tasks(self, job_information):
        for member in self.members:
            for task in member.get_tasks():
                if self.status.lower() in task.get_task_type().lower():
                    logger.debug("Executing Task of type: " + self.status)
                    try:

                        TaskExecutor.Instance().schedule_task(job_information, task)
                    except Exception, e:
                        logger.error("Error while executing: " + str(e))
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

            logger.info("Job " + self.get_job_id() +
                        ", Code: " + str(self.last_execution.get_error_code()) +
                        ", Message: " + str(self.last_execution.get_message()))

            self.job_information.set_response_message(self.last_execution.get_response_message(self))

            self.handle_tasks(self.job_information)
        else:
            logger.info("Job " + self.get_job_id() + " disabled")

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
        msg = str(job.status) + " [" + job.service.get_config_name() + ": " + str(job.get_job_id()) + "] " + \
            str(job.get_hostgroup()) + " " + str(job.get_host())
        if self.get_message() is not None:
            msg += " " + str(self.get_message())
        if self.get_kwargs() is not None:
            msg += " " + str(self.get_kwargs())
        return msg


class JobInformation(object):
    def __init__(self, job_id, hostgroup, host, service, members):
        self.job_id = job_id
        self.hostgroup = hostgroup
        self.host = host
        self.service = service
        self.members = members

        self.response_massage = None
        self.period = None
        self.next_run = None
        self.runs = 0
        self.enabled = None
        self.threshold = 0
        self.fails = 0
        self.job_overall_fails = 0
        self.job_overall_wins = 0
        self.last_execution = None
        self.last_run = None
        self.last_fail = None
        self.last_success = None
        self.last_disabled = None
        self.last_enabled = None
        self.last_threshold_override = None
        self.last_escalation = None
        self.status = "NONE"

    def inc_job_overall_fails(self):
        self.job_overall_fails += 1

    def inc_job_overall_wins(self):
        self.job_overall_wins += 1

    def get_job_id(self):
        return self.job_id

    def get_response_message(self):
        return self.response_massage

    def set_response_message(self, msg):
        self.response_massage = msg

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status