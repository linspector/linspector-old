"""
The interface class should contain all stuff for frontend/backend
communication to the Linspector core.

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

from collections import OrderedDict


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
        d["Fails"] = str(job.jobThreshold)
        return d

    def get_job_list(self):
        job_list = []
        for job in self.jobs:
            d = self.get_job_info_dict(job)
            job_list.append(d)
        return job_list

    def get_enabled_layouts(self):
        self._config.get_enabled_layouts()

    def _set_jobs_enabled(self, jobs, enabled=True):
        for job in jobs:
            job.set_enabled(enabled)

    def _compare_jobs(self, job_arg_getter, compare):
        return [job for job in self.jobs if job_arg_getter(job) == compare]

    def set_host_jobs_enabled(self, host, enabled=True):
        self._set_jobs_enabled(self._compare_jobs(lambda job: job.host, host), enabled)

    def set_hostgroup_jobs_enabled(self, hostgroupName, enabled=True):
        self._set_jobs_enabled(self._compare_jobs(lambda job: job.hostgroup.get_name(), hostgroupName), enabled)
