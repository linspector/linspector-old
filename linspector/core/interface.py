"""
The interface class should contain all stuff for frontend/backend communication to the Linspector core.

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
        for job in self.jobs:
            if job.hex_string() == hexString:
                return job

    def get_enabled_layouts(self):
        self._config.get_enabled_layouts()


