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
from Queue import Queue
from threading import Event, Thread
from linspector.utils.singleton import Singleton

KEY_TYPE = "type"
KEY_ARGS = "args"
KEY_CLASS = "class"

logger = getLogger(__name__)


class Task(object):
    def __init__(self, **kwargs):
        self._args = {}
        if KEY_ARGS in kwargs:
            self.add_arguments(kwargs[KEY_ARGS])
        elif self.needs_arguments():
            raise Exception("Error: needs arguments but none provided!")

        if KEY_CLASS in kwargs:
            self.name = kwargs[KEY_CLASS]
        else:
            self.name = self.__class__

        self._type = None
        if KEY_TYPE in kwargs:
            self._type = kwargs[KEY_TYPE]

    def get_task_type(self):
        return str(self._type)

    def get_config_name(self):
        return str(self.name)

    def add_arguments(self, args):
        for key, val in args.items():
            self._args[key] = val

    def get_arguments(self):
        return self._args

    def set_member(self, member):
        self.member = member

    def needs_arguments(self):
        return False

    def execute(self, job):
        try:
            self.execute(job)
        except Exception, e:
            logger.debug("Task execute failed!!!")
            raise e


@Singleton
class TaskExecutor(object):
    def __init__(self):
        self.queue = Queue()
        self.taskInfos = []
        task_thread = Thread(target=self._run_worker_thread)
        self._instantEnd = False
        self._running = True
        task_thread.daemon = True
        task_thread.start()

    def _run_worker_thread(self):
        while self.is_running() or not self.is_instant_end():

            try:
                msg, task = self.queue.get()
                if task:
                    logger.debug("Starting Task Execution...")
                    task.execute(msg)
                self.queue.task_done()

            except Exception, e:
                logger.error("Error " + str(e))

    def is_instant_end(self):
        return self._instantEnd

    def is_running(self):
        return self._running

    def stop(self):
        self._running = False

    def stop_immediately(self):
        self._running = False
        self._instantEnd = True

    def schedule_task(self, msg, task):
        self.queue.put((msg, task))