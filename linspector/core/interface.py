"""
The interface class should contain all stuff for frontend/backend
communication to the Linspector core.

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

from collections import OrderedDict
from logging import getLogger

logger = getLogger(__name__)


class LinspectorInterface(object):
    def __init__(self, jobs, scheduler, linspectorConfig):
        self.jobs = jobs
        self._scheduler = scheduler
        self._config = linspectorConfig
        self._recompute_job_hex_strings()

    def _recompute_job_hex_strings(self):
        self.jobHex = []
        for job in self.jobs:
            self.jobHex.append(job.hex_string())

    def get_job_hex_strings(self):
        return self.jobHex

    def find_job_by_hex_string(self, hexString):
        if hexString is None:
            return None
        for job in self.jobs:
            if job.hex_string() == hexString:
                return job

    def get_job_info_dict(self, job):
        d = OrderedDict()
        d["Job"] = job.hex_string()
        d["Hostgroup"] = job.hostgroup.get_name()
        d["Host"] = job.host
        d["Service"] = str(job.service)
        d["Members"] = str([member.name for member in job.members])
        d["Period"] = str(job.job.trigger)
        d["Next run"] = str(job.job.next_run_time)
        d["Runs"] = str(job.job.runs)
        d["Enabled"] = str(job._enabled)
        d["Threshold"] = str(job.service.get_threshold())
        d["Fails"] = str(job.jobThreshold)
        #d["Last Run"] = None
        #d["Last Fail"] = None
        #d["Last Success"] = None
        #d["Last Disabled"] = None
        #d["last Enabled"] = None
        #d["Last Threshold Override"] = None
        #d["Last Escalation"] = None
        return d

    def get_job_list(self):
        job_list = []
        for job in self.jobs:
            d = self.get_job_info_dict(job)
            job_list.append(d)
        return job_list

    def get_job_list_by_hostgroup(self, hostgroup):
        job_list = []
        for job in self.jobs:
            if hostgroup == job.hostgroup.get_name():
                d = self.get_job_info_dict(job)
                job_list.append(d)
        return job_list

    def get_job_list_by_host(self, host):
        job_list = []
        for job in self.jobs:
            if host == job.host:
                d = self.get_job_info_dict(job)
                job_list.append(d)
        return job_list

    def get_job_count(self):
        count = len(self.jobs)
        return count

    def get_job_count_by_hostgroup(self, hostgroup):
        job_count = 0
        for job in self.jobs:
            if hostgroup == job.hostgroup.get_name():
                job_count += 1
        return job_count

    def get_job_count_by_host(self, host):
        job_count = 0
        for job in self.jobs:
            if host == job.host:
                job_count += 1
        return job_count

    def _set_jobs_enabled(self, jobs, enabled=True):
        for job in jobs:
            job.set_enabled(enabled)

    def _compare_jobs(self, job_arg_getter, compare):
        return [job for job in self.jobs if job_arg_getter(job) == compare]

    def set_host_jobs_enabled(self, host, enabled=True):
        self._set_jobs_enabled(self._compare_jobs(lambda job: job.host, host), enabled)

    def set_hostgroup_jobs_enabled(self, hostgroupName, enabled=True):
        self._set_jobs_enabled(self._compare_jobs(lambda job: job.hostgroup.get_name(), hostgroupName), enabled)

    def get_hostgroup_list(self):
        pass

    def get_hostgroup_count(self):
        pass

    def get_host_list(self):
        pass

    def get_host_list_by_hostgroup(self, hostgroup):
        pass

    def get_host_count(self):
        pass

    def get_host_count_by_hostgroup(self, hostgroup):
        pass

    def get_services_by_hostgroup(self, hostgroup):
        pass

    def get_services_by_host(self, host):
        pass

    def get_service_count_by_hostgroup(self, hostgroup):
        pass

    def get_service_count_by_host(self, host):
        pass

    def get_enabled_layouts(self):
        self._config.get_enabled_layouts()

    def get_thread_count(self):
        return {"Num Threads": str(self._scheduler._threadpool.num_threads),
                "Max Threads": str(self._scheduler._threadpool.max_threads)}