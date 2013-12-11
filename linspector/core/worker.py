"""
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

from logging import getLogger
from multiprocessing import Process

from linspector.core.job import LinspectorJob
from linspector.core.scheduler import LinspectorScheduler

logger = getLogger(__name__)


class LinspectorWorker(Process):
    def __init__(self, core_threads, max_threads):
        super(LinspectorWorker, self).__init__()

        self.core_threads = core_threads
        self.max_threads = max_threads

        self.scheduler = LinspectorScheduler({"apscheduler.threadpool.core_threads": self.core_threads,
                                              "apscheduler.threadpool.max_threads": self.max_threads})
        self.scheduler.standalone = True

    def run(self):
        self.scheduler.start()

    @staticmethod
    def handle_job(job):
        job.handle_call()

    def get_name(self):
        return self._name

    def get_scheduler(self):
        return self.scheduler

    def shutdown(self, wait=True):
        self.scheduler.shutdown(wait=wait)

    def create_job(self, jobs, service, host, hostgroup, core, period, start_date=None, executor=None):
        job = LinspectorJob(service, host, hostgroup.get_members(), core, hostgroup, executor)
        scheduler_job = period.createJob(self.scheduler, job, self.handle_job, start_date=start_date)
        if scheduler_job is not None:
            job.set_job(scheduler_job)
            jobs.append(job)