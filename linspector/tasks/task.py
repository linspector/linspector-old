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
from Queue import Queue
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
        logger.debug("init taskExecutor")
        self.event = Event()
        self.taskInfos = Queue()
        task_thread = Thread(target=self._run_worker_thread)
        self._instantEnd = False
        self._running = True
        task_thread.daemon = True
        task_thread.start()

    def _run_worker_thread(self):
        logger.debug("start running taskExcecutor worker Thread")
        while self.is_running() or not self.is_instant_end():
            '''
            if len(self.taskInfos) == 0:
                logger.debug("waiting for jobs to add")
                self.event.clear()
                self.event.wait()
                logger.debug("Task Executor waked up")

            try:
                logger.debug("trying to get task information")
                msg, task = self.taskInfos[0]
                del self.taskInfos[0]
                if task:
                    logger.debug("Starting Task Execution of task: %s", str(task))
                    task.execute(msg)

            except Exception, e:
                logger.error("Error " + str(e))
            '''
            try:
                logger.debug("try to get queued task")
                msg, task = self.taskInfos.get()
                logger.debug("got task %s for msg: %s", str(task), str(msg))
                task.execute(msg)
            except Exception, e:
                logger.error("Error " + str(e))
        logger.debug("shutting down TaskExecutor!")

    def is_instant_end(self):
        return self._instantEnd

    def is_running(self):
        return self._running

    def stop(self):
        self._running = False
        self.event.set()

    def stop_immediately(self):
        self._running = False
        self._instantEnd = True
        self.event.set()

    def schedule_task(self, msg, task):
        try:
            logger.debug("appending task '%s' for msg: %s", str(task), str(msg))
            self.taskInfos.put((msg, task))
        except Exception, e:
            logger.debug("queue is probably full: %s", str(e))
        #logger.debug("%s task Queued", str(len(self.taskInfos)))
        #self.event.set()
