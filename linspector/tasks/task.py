"""
The task classes.

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
from threading import Event, Thread


logger = getLogger(__name__)


class Task:
    def raise_config_exception(self, typeDict, name):
        raise Exception("typeDict " + str(typeDict) + " has no " + str(name) + " argument!")

    def set_task_type(self, taskType):
        self._taskType = taskType
        return self

    def get_task_type(self):
        return self._taskType

    def execute(self, msg, args):
        pass


class TaskList(object):
    def __init__(self, tasks):
        self.tasks = tasks
        self.event = Event()
        self.taskInfos = []
        task_thread = Thread(target=self._run_worker_thread)
        task_thread.setDaemon(True)
        task_thread.start()

    def _run_worker_thread(self):
        while True:
            if len(self.taskInfos) == 0:
                self.event.clear()
                self.event.wait()
            msg, taskInfos = self.taskInfos[0]
            del self.taskInfos[0]
            try:
                for taskInfo in taskInfos:
                    task = self.find_task_by_name(taskInfo["class"])
                    if task:
                        task.execute(msg, taskInfo["args"])
            except:
                pass

    def find_task_by_name(self, clazzName):
        for task in self.tasks:
            if task.get_task_type() == clazzName:
                return task

    def execute_task_infos(self, msg, taskInfos):
        self.taskInfos.append((msg, taskInfos))
        self.event.set()