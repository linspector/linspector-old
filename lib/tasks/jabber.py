"""
The Jabber (XMPP) task.

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

    def execute(self, msg, core):
        #TODO: totally unstable just to use values from core. make checks before...!
        client = xmpp.Client(core["tasks"]["jabber"]["host"], core["tasks"]["jabber"]["port"], None)
        client.connect(server=(core["tasks"]["jabber"]["host"], core["tasks"]["jabber"]["port"]))
        client.auth(core["tasks"]["jabber"]["username"], core["tasks"]["jabber"]["password"], 'alert')
        client.sendInitPresence()
        message = xmpp.Message(self.recipient, msg)
        message.setAttr('type', 'chat')
        client.send(message)


def create(taskDict):
    return JabberTask(**taskDict)