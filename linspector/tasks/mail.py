"""
The mail task.

http://docs.python.org/2/library/email-examples.html#

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

import datetime
import smtplib

from email.mime.text import MIMEText
from logging import getLogger

from linspector.tasks.task import Task

logger = getLogger(__name__)


class MailTask(Task):
    def __init__(self, **kwargs):
        if not "type" in kwargs:
            raise Exception("'type' not in typeDict " + str(kwargs))
        if not "args" in kwargs:
            raise Exception("typeDict " + str(kwargs) + " has no arguments!")
        self.set_task_type(kwargs["type"])
        self.recipient = kwargs["args"]["rcpt"]

    def execute(self, msg, core):
        message = MIMEText(msg)
        message['Subject'] = msg
        now = datetime.datetime.now()
        message['Date'] = now.strftime("%a, %d %b %Y %H:%M:%S")
        #TODO: totally unstable just to use values from core. make checks before...!
        message['From'] = core["tasks"]["mail"]["from"]
        message['To'] = self.recipient
        s = smtplib.SMTP(core["tasks"]["mail"]["host"], core["tasks"]["mail"]["port"])
        s.login(core["tasks"]["mail"]["username"], core["tasks"]["mail"]["password"])
        s.sendmail(core["tasks"]["mail"]["from"], self.recipient, message.as_string())
        s.quit()


def create(taskDict):
    return MailTask(**taskDict)