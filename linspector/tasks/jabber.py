"""
The Jabber (XMPP) task.

Uses: http://xmpppy.sourceforge.net/

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

import xmpp

from logging import getLogger

from linspector.tasks.task import Task

logger = getLogger(__name__)


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