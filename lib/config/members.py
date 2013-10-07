"""
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

import re


class Member:
    def __init__(self, id, name="",  comment="", tasks=None):
        self.id = id
        self.name = name
        self.tasks = []
        self.add_task(tasks)
        self.comment = comment

    def get_id(self):
        return self.id

    def add_task(self, task):
        if task is None:
            return
        if isinstance(task, list):
            self.tasks.extend(task)
        else:
            self.tasks.append(task)
    
    def get_tasks(self):
        return self.tasks

    def __str__(self):
        ret = "Member Id: " + self.nameid + " Name: " + self.name + " Filters: " + str(self.phone)
        for f in self.filters:
            ret += str(f)
        return ret


class MemberFilter:
    def __init__(self, filter, Value):
        self.filter = filter
        self.value = Value

    def __str__(self):
        return "Filter:" + str(self.filter) + " Value:" + self.value


def parseMemberList(members, filters, log):
    parsedMembers = [Member(nameid, **values) for nameid, values in members.items()]
    for member in parsedMembers:
        mFilter = []
        for filtername, replacement in member.filters.items():
            found = False
            for filt in filters:
                if filt.name != filtername:
                    continue
                found = True
                memberFilter = filt.clone()
                memberFilter.command = re.sub('@member', replacement, filt.command)
                mFilter.append(memberFilter)
            if not found:
                log.w("filter: " + filtername + " is not defined in member " + member.name)
        member.filters = mFilter
    return parsedMembers