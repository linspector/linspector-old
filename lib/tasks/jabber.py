"""
The Jabber task.

Uses: http://xmpppy.sourceforge.net/
"""

import xmpp
from lib.tasks.task import Task


class JabberTask(Task):
    def __init__(self, **kwargs):
        if not "type" in kwargs:
            raise Exception("'type' not in typeDict " + str(kwargs))
        if not "args" in kwargs:
            raise Exception("typeDict " + str(kwargs) + " has nor arguments!")
        self.set_task_type(kwargs["type"])
        self.recipient = kwargs["args"]["rcpt"]

    def execute(self, msg):
        client = xmpp.Client('systemchaos.org')
        client.connect(server=('systemchaos.org', 5222))
        client.auth('linspector', 'PASSWORD', 'alert')
        client.sendInitPresence()
        message = xmpp.Message('hanez@systemchaos.org', msg)
        message.setAttr('type', 'chat')
        client.send(message)


def create(taskDict):
    return JabberTask(**taskDict)