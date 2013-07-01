"""
The task class.
"""


class Task:
    """
    Base class for all built-in Tasks.
    """

    def set_task_type(self, taskType):
        self._taskType = taskType

    def get_task_type(self):
        """
        :return: the type set by set_type_task
        """
        return self._taskType

    def some_other_irrelevant_methods(self):
        pass