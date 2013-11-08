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

logger = getLogger(__name__)


class MemberException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class MemberMissingArgumentException(MemberException):
    def __init__(self, missingArgument, memberName):
        super(MemberMissingArgumentException, self).__init__("no " + missingArgument + " defined for member " + memberName)


class Member:
    def __init__(self, name="", **kwargs):
        self.name = name
        tmp = "tasks"
        self.tasks = []
        if not tmp in kwargs:
            raise MemberMissingArgumentException(tmp, name)
        self.add_tasks(kwargs[tmp])

    def __add_internal(self, l, item):
        if isinstance(item, list):
            l.extend(item)
        else:
            l.append(item)

    def add_tasks(self, tasks):
        self.__add_internal(self.get_tasks(), tasks)
    
    def get_tasks(self):
        return self.__tasks

    def __str__(self):
        ret = "Member: " + self.name + " Tasks: "
        for t in self.tasks:
            ret += str(t)
        return ret