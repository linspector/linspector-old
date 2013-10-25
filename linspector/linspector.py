"""
The Linspector main thread. Here all scheduling is done so backends and
frontends can start before all jobs are scheduled.

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

import threading
import time

from core.job import Job


def handle_job(jobInfo):
    jobInfo.handle_call()


class Linspector(threading.Thread):
    def __init__(self, linConf, core, scheduler, log, q):
        self.linConf = linConf
        self.core = core
        self.scheduler = scheduler
        self.log = log
        self.q = q
        threading.Thread.__init__(self)

    def handle_job(self, jobInfo):
        jobInfo.handle_call()

    def run(self):
        jobs = []
        for layout in self.linConf.get_enabled_layouts():
            for hostgroup in layout.get_hostgroups():
                for service in hostgroup.get_services():
                    for host in hostgroup.get_hosts():
                        for period in service.get_periods():
                            job = Job(service,
                                      host,
                                      hostgroup.get_members(),
                                      hostgroup.get_processors(),
                                      self.core,
                                      hostgroup)
                            schedulerJob = period.createJob(self.scheduler, job, handle_job)
                            if schedulerJob is not None:
                                job.set_job(schedulerJob)
                                job.set_logger(self.log)
                                jobs.append(job)
                                self.q.put(jobs)
                                time.sleep(3)