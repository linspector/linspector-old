"""
The xmpp task.
"""

from task import Task


class XmppTask(Task):
    def __init__(self, **kwargs):
        if not "type" in kwargs:
            raise Exception("'type' not in typeDict " + str(kwargs))
        if not "args" in kwargs:
            raise Exception("typeDict " + str(kwargs) + " has nor arguments!")
        self.set_task_type(kwargs["type"])
        self.recipient = kwargs["args"]["rcpt"]

    def execute_task(self, msg):
        pass


def create(taskDict):
    return XmppTask(**taskDict)