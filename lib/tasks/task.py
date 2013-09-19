"""
The task class.
"""


class Task:
    def set_task_type(self, taskType):
        self._taskType = taskType

    def get_task_type(self):
        return self._taskType

    def execute(self, msg):
        pass